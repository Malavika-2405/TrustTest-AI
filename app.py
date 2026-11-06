
import os
import textwrap

from dotenv import load_dotenv
import streamlit as st

# Load environment configuration
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="TrustTest AI | LLM Quality Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import application modules
from database.db import init_db
from modules.conversation_testing import render_conversation_testing
from modules.dashboard import render_dashboard
from modules.dataset_manager import render_dataset_manager
from modules.evaluation_engine import render_evaluation_engine
from modules.regression_testing import render_regression_testing
from modules.reports import render_reports
from modules.safety_testing import render_safety_testing
from modules.automated_test_runner import render_automated_test_runner


# Initialize database
init_db()


# Professional Dark SaaS Theme
st.markdown(
    """
    <style>
        /* Main application background */
        .stApp {
            background-color: #080D19;
            color: #FFFFFF;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0D1525;
            border-right: 1px solid #243047;
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }

        /* Main text visibility */
        .stApp,
        .stApp p,
        .stApp label,
        .stApp li,
        .stApp span,
        .stApp .stMarkdown {
            color: #F1F5F9;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }

        /* Sidebar text */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #F1F5F9;
        }

        /* Captions and secondary text */
        .stCaption,
        [data-testid="stCaptionContainer"] {
            color: #CBD5E1 !important;
        }

        /* Sidebar navigation */
        [data-testid="stSidebar"] [role="radiogroup"] label {
            color: #F1F5F9 !important;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background-color: #111D30;
            border: 1px solid #263650;
            padding: 18px;
            border-radius: 12px;
        }

        [data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            font-weight: 700;
        }

        [data-testid="stMetricLabel"] {
            color: #E2E8F0 !important;
        }

        [data-testid="stMetricDelta"] {
            color: #86EFAC !important;
        }

        /* Buttons */
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
            color: #FFFFFF;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6D28D9, #0284C7);
            border: none;
            color: #FFFFFF !important;
        }

        .stButton > button[kind="primary"]:hover {
            opacity: 0.88;
            border: none;
        }

        /* Input fields */
        input, textarea {
            color: #FFFFFF !important;
            background-color: #111D30 !important;
        }

        /* Select boxes */
        div[data-baseweb="select"] {
            color: #FFFFFF !important;
        }

        /* Data tables */
        [data-testid="stDataFrame"] {
            border: 1px solid #263650;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            border: 1px solid #263650;
            border-radius: 10px;
        }

        /* Input borders */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            border-radius: 8px;
        }

        /* Main content spacing */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Dividers */
        hr {
            border-color: #334155;
        }

        /* Sidebar branding secondary text */
        [data-testid="stSidebar"] small {
            color: #CBD5E1 !important;
        }

        /* Links */
        a {
            color: #7DD3FC !important;
        }

        /* Success and information messages */
        [data-testid="stAlert"] {
            color: #FFFFFF !important;
        }

        /* Placeholder text */
        input::placeholder,
        textarea::placeholder {
            color: #A8B6CC !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


def main():

    # Sidebar
    with st.sidebar:

        # Sidebar Branding
        st.markdown(
            textwrap.dedent("""
                <div style="display:flex; align-items:center; gap:12px; padding:8px 0 18px 0;">
                    <div style="font-size:32px; background:#172A46; padding:9px; border-radius:12px;">
                        🛡️
                    </div>
                    <div>
                        <div style="font-size:22px; font-weight:750; color:#FFFFFF;">
                            TrustTest AI
                        </div>
                        <div style="font-size:11px; color:#CBD5E1; letter-spacing:1px;">
                            LLM QUALITY PLATFORM
                        </div>
                    </div>
                </div>
            """),
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("##### WORKSPACE")

        # Navigation
        menu = st.radio(
            "Navigation",
            [
                "📊 Overview Dashboard",
                "📚 Golden Dataset Management",
                "🧪 Run Evaluations",
                "🧰 Automated Test Runner",
                "🔄 Automated Regression",
                "🛡️ AI Safety & Injections",
                "💬 Multi-Turn Consistency",
                "📑 Quality Reports",
            ],
            index=0,
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Engine Configuration
        st.markdown("##### ⚙️ ENGINE CONFIGURATION")

        st.caption(
            "Semantic evaluation currently runs locally "
            "using Sentence Transformers."
        )

        current_api_key = os.getenv("OPENAI_API_KEY", "")

        new_key = st.text_input(
            "OpenAI API Key (Optional)",
            value=current_api_key,
            type="password",
            help="Optional. Not required for local semantic similarity evaluation.",
        )

        if new_key != current_api_key:
            if new_key.strip():
                os.environ["OPENAI_API_KEY"] = new_key.strip()
                st.success("API key configured for this session.")
            else:
                os.environ.pop("OPENAI_API_KEY", None)
                st.info("API key cleared for this session.")

        st.markdown("---")

        # Sidebar Footer
        st.markdown(
            textwrap.dedent("""
                <div style="padding:10px 0; color:#CBD5E1; font-size:12px; line-height:1.8;">
                    <b style="color:#FFFFFF;">TrustTest AI</b><br>
                    Version 1.0.0<br>
                    LLM Quality & Reliability Testing
                    <br><br>
                    <span style="color:#A8B6CC;">
                        Test Smarter. Trust AI.
                    </span>
                </div>
            """),
            unsafe_allow_html=True,
        )

    # Main Application Header
    st.markdown(
        textwrap.dedent("""
            <div style="padding:16px 0 20px 0; border-bottom:1px solid #263650; margin-bottom:24px;">
                <div style="font-size:13px; color:#38BDF8; font-weight:600; letter-spacing:1.5px;">
                    AI QUALITY ASSURANCE WORKSPACE
                </div>
                <div style="font-size:25px; font-weight:700; color:#FFFFFF; margin-top:5px;">
                    LLM Testing & Reliability Platform
                </div>
                <div style="font-size:13px; color:#CBD5E1; margin-top:5px;">
                    Evaluate, monitor and improve AI response quality.
                </div>
            </div>
        """),
        unsafe_allow_html=True,
    )

    # Application Navigation
    if menu == "📊 Overview Dashboard":
        render_dashboard()

    elif menu == "📚 Golden Dataset Management":
        render_dataset_manager()

    elif menu == "🧪 Run Evaluations":
        render_evaluation_engine()

    elif menu == "🧰 Automated Test Runner":
        render_automated_test_runner()

    elif menu == "🔄 Automated Regression":
        render_regression_testing()

    elif menu == "🛡️ AI Safety & Injections":
        render_safety_testing()

    elif menu == "💬 Multi-Turn Consistency":
        render_conversation_testing()

    elif menu == "📑 Quality Reports":
        render_reports()


if __name__ == "__main__":
    main()
