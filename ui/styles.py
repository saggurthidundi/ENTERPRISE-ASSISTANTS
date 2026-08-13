def load_custom_css():
  return """
    <style>
    @keyframes geminiGlow {
        0% { filter: drop-shadow(0 0 2px rgba(66, 133, 244, 0.3)); }
        50% { filter: drop-shadow(0 0 12px rgba(155, 114, 203, 0.6)); }
        100% { filter: drop-shadow(0 0 2px rgba(66, 133, 244, 0.3)); }
    }
    @keyframes cardFloat {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }
    .stApp {
        background: linear-gradient(180deg, #0b0f19 0%, #05070b 100%);
        color: #e3e3e3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #0d111a;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
        background-color: transparent;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #121824;
        border-radius: 14px;
        padding: 12px 24px;
        color: #8ab4f8;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1a2233;
        color: #ffffff;
        border-color: rgba(66, 133, 244, 0.4);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4285f4 0%, #9b72cb 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(66, 133, 244, 0.4);
    }
    .ai-card {
        background: rgba(18, 24, 36, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 30px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 24px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        animation: cardFloat 6s ease-in-out infinite;
    }
    .ai-card:hover {
        border-color: rgba(155, 114, 203, 0.5);
        box-shadow: 0 20px 50px rgba(66, 133, 244, 0.15);
        transform: translateY(-2px);
    }
    .stButton>button {
        background: linear-gradient(135deg, #1a2233 0%, #25304a 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 14px 32px;
        font-weight: 600;
        border: 1px solid rgba(66, 133, 244, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4285f4 0%, #9b72cb 100%);
        border-color: transparent;
        box-shadow: 0 8px 25px rgba(155, 114, 203, 0.5);
        transform: scale(1.02);
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #0f1520 !important;
        color: #f0f6fc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 14px !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4285f4 !important;
        box-shadow: 0 0 20px rgba(66, 133, 244, 0.3) !important;
    }
    [data-testid="stMetric"] {
        background: rgba(18, 24, 36, 0.5);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """