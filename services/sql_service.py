import time
import re
from sqlalchemy import text
from database.connection import SessionLocal
from langchain_google_genai import ChatGoogleGenerativeAI

def run_sql_query(db_uri, api_key, query_text):
  models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]
  last_exception = None

  db_session = SessionLocal()
  schema_info = ""
  try:
    tables_result = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    tables = [row[0] for row in tables_result]
    schema_info += f"Tables: {', '.join(tables)}. "
    for table in tables:
      columns = db_session.execute(text(f"PRAGMA table_info({table});")).fetchall()
      col_names = [col[1] for col in columns]
      schema_info += f"Table {table} has columns: {', '.join(col_names)}. "
  except Exception:
    schema_info = "Schema unavailable."
  finally:
    db_session.close()

  # Prompt enforces safe, structured read-only generation
  prompt = f"""
You are an expert SQLite data analyst. 
Schema: {schema_info}
User Request: {query_text}

CRITICAL SECURITY RULE: You must generate ONLY a safe, structured, read-only SELECT statement.
Provide ONLY the raw SQLite query text without any markdown ticks, formatting, or commentary.
"""

  sql_query = ""
  for model_name in models_to_try:
    try:
      llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0)
      response = llm.invoke(prompt)
      
      raw_content = response.content
      if isinstance(raw_content, list):
        content = "".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in raw_content])
      elif isinstance(raw_content, dict):
        content = raw_content.get("text", str(raw_content))
      else:
        content = str(raw_content)
      
      sql_query = content.replace("```sql", "").replace("```", "").strip()
      if sql_query:
        break
    except Exception as e:
      last_exception = e
      if any(code in str(e) for code in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]):
        time.sleep(2)
        continue

  if not sql_query:
    if last_exception:
      raise last_exception
    return "Could not generate a query."

  # STRICT SECURITY SAFEGUARDS
  clean_query = sql_query.rstrip(";")
  upper_query = clean_query.upper().strip()

  # Rule 1: Query MUST start with SELECT
  if not upper_query.startswith("SELECT"):
      return "Security restriction: Only safe, structured SELECT queries are permitted."

  # Rule 2: Block any data manipulation or definition keywords
  forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "REPLACE", "CREATE", "GRANT", "REVOKE"]
  
  for keyword in forbidden_keywords:
      # Use regex word boundaries to prevent bypassing (e.g., matching "DROP" but allowing a column named "backdrop")
      if re.search(r'\b' + keyword + r'\b', upper_query):
          return f"Security restriction: The keyword '{keyword}' is not allowed. Only read operations are permitted."

  session = SessionLocal()
  try:
    result = session.execute(text(clean_query))
    rows = result.fetchall()
    keys = result.keys()
    
    if not rows:
      return "The safe structured query executed successfully, but found no matching records."

    sentences = ["Here are the results found in the database:"]
    for row in rows[:15]:
      pair_text = " with ".join([f"{key} being {val}" for key, val in zip(keys, row)])
      sentences.append(f"There is a record where {pair_text}.")
      
    return " ".join(sentences)

  except Exception as db_err:
    return f"An error occurred while executing the database query: {str(db_err)}"
  finally:
    session.close()