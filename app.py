from config.settings import APP_TITLE, DEFAULT_DB_URI
from database.connection import engine
from database.models import Base
from ui.components import render_footer, render_header
from ui.sidebar import render_sidebar
from ui.styles import load_custom_css
import streamlit as st

def main():
    # Initialize database tables
    Base.metadata.create_all(bind=engine)

    st.set_page_config(
        page_title="AI Enterprise Assistant", 
        page_icon="✦", 
        layout="wide"
    )
    
    st.markdown(load_custom_css(), unsafe_allow_html=True)

    api_key, db_uri, active_tab = render_sidebar(DEFAULT_DB_URI)

    if not api_key:
        st.warning("⚠️ Please paste your Google Gemini API Key in the sidebar control panel to unlock the workspace.")
        st.stop()

    render_header(APP_TITLE)

    if active_tab == "📄 Intelligent Document RAG":
        from ui.components import render_rag_tab
        render_rag_tab(api_key)
    elif active_tab == "📊 Structured SQL Agent":
        from ui.components import render_sql_tab
        render_sql_tab(db_uri, api_key)
    else:
        from ui.components import render_metrics_tab
        render_metrics_tab()

    render_footer()

if __name__ == "__main__":
    main()