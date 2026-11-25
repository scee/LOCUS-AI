
import streamlit as st
from pathlib import Path

# =========================================
# CONFIGURATION
# =========================================

st.set_page_config(
    page_title="LOCUS AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

   
# Load custom CSS
css_path = Path("styles/main.css")

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text()}</style>",
        unsafe_allow_html=True
    )

    st.sidebar.divider()

dark_mode = st.sidebar.toggle(
    "Dark Mode",
    value=False,
    key="dark_mode"
)

if st.session_state["dark_mode"]:
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
            --locus-bg: #101820;
            --locus-surface: #1B2732;
            --locus-surface-alt: #263746;
            --locus-dark: #F4F7F9;
            --locus-text: #E2E8F0;
            --locus-muted: #A0AEC0;
            --locus-border: #344454;
            }

            [data-testid="stAppViewContainer"] {
                background-color: var(--locus-bg);
                color: var(--locus-text);
            }

            [data-testid="stSidebar"] {
                background-color: var(--locus-surface);
                border-color: var(--locus-border);
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: var(--locus-surface);
                border-color: var(--locus-border);
            }

            h1, h2, h3, h4, p, label, span {
                color: var(--locus-text);
            }

            [data-testid="stMetric"] {
                background-color: var(--locus-surface);
                padding: 1rem;
                border-radius: 10px;
            }

            hr {
                border-color: var(--locus-border);
            }
        </style>
    """, unsafe_allow_html=True)

else:
    ## LIGHT MODE
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
            --locus-bg: #F4F7F9;
            --locus-surface: #FFFFFF;
            --locus-surface-alt: #EDF2F5;
            --locus-dark: #101820;
            --locus-text: #263746;
            --locus-muted: #718096;
            --locus-border: #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)


# =========================================
# PAGE COMPONENTS
# =========================================

def page_header(title, description):
    with st.container(key="main_header"):
        st.markdown(f"## {title}")
        st.caption(description)


def placeholder_page(title, description):
    page_header(title, description)

    st.info(
        "Esta área está em desenvolvimento. "
        "Os conteúdos serão disponibilizados nesta secção."
    )


# =========================================
# PAGES
# =========================================

def dashboard():
    page_header(
        "Dashboard",
        "Visão geral da Inteligência Territorial."
    )

    st.markdown("### Bem-vindo ao LOCUS AI")

    st.write(
        "Explore dados territoriais, analise indicadores "
        "e descubra padrões através da Ciência de Dados "
        "e Inteligência Artificial."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Indicadores", "—", help="Aguardando integração de dados")

    with col2:
        st.metric("Territórios", "—", help="Aguardando integração de dados")

    with col3:
        st.metric("Modelos disponíveis", "—", help="Em desenvolvimento")


def territorial_explorer():
    placeholder_page(
        "Territorial Explorer",
        "Explore a informação territorial de forma geográfica."
    )


def comparisons():
    placeholder_page(
        "Comparisons",
        "Compare indicadores entre diferentes territórios."
    )


def statistical_analysis():
    placeholder_page(
        "Statistical Analysis",
        "Explore relações, distribuições e tendências nos dados."
    )


def clustering():
    placeholder_page(
        "Clustering",
        "Identifique grupos e padrões territoriais."
    )


def predictions():
    placeholder_page(
        "Predictions",
        "Explore previsões e tendências com modelos de IA."
    )


# =========================================
# NAVIGATION
# =========================================

st.sidebar.markdown(
    """
    <div style="padding: 0.8rem 0 1.5rem 0;">
        <div style="font-size: 1.7rem; font-weight: 800;">
            <span style="color:#00B8D9;">LOCUS</span>
            <span style="color:#101820;">AI</span>
        </div>
        <div style="font-size:0.75rem; color:#718096; letter-spacing:1px;">
            TERRITORIAL INTELLIGENCE
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

pages = {
    "Overview": [
        st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True),
    ],
    "Explore": [
        st.Page("pages/territorial_intelligence.py", title="Territorial Intelligence", icon=":material/analytics:"),
        st.Page("pages/territorial_explorer.py", title="Territorial Explorer", icon=":material/map:"),
        st.Page("pages/comparisons.py", title="Comparisons", icon=":material/compare_arrows:"),
    ],
    "Analytics": [
        
        st.Page("pages/statistical_analysis.py", title="Statistical Analysis", icon=":material/analytics:"),
        st.Page("pages/clustering.py", title="Clustering", icon=":material/hub:"),
        st.Page("pages/predictions.py", title="Predictions", icon=":material/insights:"),
    ],
}

pg = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)




pg = st.navigation(pages)
pg.run()


