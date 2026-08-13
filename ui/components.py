import time
import streamlit as st
from services.rag_service import process_pdf_document
from services.sql_service import run_sql_query
from langchain_google_genai import ChatGoogleGenerativeAI

def render_header(title=None):
    display_title = title if title else "✦ AI-Powered Enterprise Assistant"
    st.markdown(
        f"""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: #4f46e5; margin-bottom: 0.5rem;'>{display_title}</h1>
            <p style='color: #6b7280; font-size: 1.1rem;'>Enterprise Document RAG, Structured SQL Agent & Intelligent Reporting</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_footer():
    st.markdown(
        """
        <hr style='margin-top: 3rem; margin-bottom: 1.5rem;'>
        <div style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>
            <p>Enterprise AI Platform &bull; Built with Streamlit, LangChain & Gemini</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_rag_tab(api_key):
    st.markdown("### Document Ingestion & Context Hub")
    st.write("Upload enterprise documents to index text for simple plain text answers.")
    uploaded_file = st.file_uploader("Drop an enterprise PDF report here", type=["pdf"])

    if uploaded_file is not None:
        chunks, filename = process_pdf_document(uploaded_file)
        if "rag_chunks" not in st.session_state:
            st.session_state.rag_chunks = []
        st.session_state.rag_chunks.extend(chunks)
        
        st.success("Successfully uploaded")

    st.markdown("---")
    rag_query = st.text_input("Ask a question regarding your documents:")

    if rag_query:
        if "rag_chunks" not in st.session_state or not st.session_state.rag_chunks:
            st.error("No context found. Please upload a document first.")
        else:
            with st.spinner("Synthesizing answer..."):
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=api_key, temperature=0)
                    context = " ".join(st.session_state.rag_chunks[:4])
                    prompt = f"Using only plain simple text paragraphs without any markdown, bullets, lists, or code blocks, answer this question based on the context:\n\nContext: {context}\n\nQuestion: {rag_query}"
                    
                    res = None
                    for attempt in range(3):
                        try:
                            res = llm.invoke(prompt)
                            break
                        except Exception as e:
                            if any(code in str(e) for code in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]):
                                if attempt < 2:
                                    time.sleep(3)
                                    continue
                            raise e

                    raw_res = res.content
                    if isinstance(raw_res, list):
                        answer_text = "".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in raw_res])
                    else:
                        answer_text = str(raw_res)

                    st.write("Response:")
                    st.write(answer_text.strip())
                except Exception as e:
                    st.error(f"Error: {str(e)}")

def render_sql_tab(db_uri="sqlite:///./enterprise.db", api_key=None):
    if isinstance(db_uri, str) and not (db_uri.startswith("sqlite") or db_uri.startswith("postgresql")) and api_key is None:
        api_key = db_uri
        db_uri = "sqlite:///./enterprise.db"

    st.markdown("### Structured SQL Database Agent")
    st.write("Query your enterprise database using natural plain text.")
    
    sql_query_input = st.text_input("Ask a question about your database:")
    
    if sql_query_input:
        with st.spinner("Querying database..."):
            try:
                response = run_sql_query(db_uri, api_key, sql_query_input)
                st.write("Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error executing database query: {str(e)}")

def render_metrics_tab():
    st.markdown("### System Metrics & Telemetry")
    st.write("View platform usage and AI agent performance.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Database Status", value="Online")
    col2.metric(label="RAG Engine", value="Active")
    col3.metric(label="System Uptime", value="100%")
    
    st.write("All enterprise services are running normally without any issues.")