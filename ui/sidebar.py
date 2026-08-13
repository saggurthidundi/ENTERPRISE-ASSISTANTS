import config.settings as settings
import streamlit as st

def render_sidebar(default_db_uri):
  st.sidebar.title("🛠️ System Settings")
  
  settings.GEMINI_API_KEY = st.sidebar.text_input(
      "Google Gemini API Key",
      type="password",
      help="Paste your Gemini API key directly here",
      value=settings.GEMINI_API_KEY if settings.GEMINI_API_KEY else ""
  )
  
  db_uri = st.sidebar.text_input("Database URI", value=default_db_uri)

  st.sidebar.markdown("---")
  st.sidebar.markdown("### 🧭 Workspace Navigation")
  selected_tab = st.sidebar.radio(
      "Choose Module",
      [
          "📄 Intelligent Document RAG",
          "📊 Structured SQL Agent",
          "⚡ System Metrics",
      ],
  )
  return settings.GEMINI_API_KEY, db_uri, selected_tab