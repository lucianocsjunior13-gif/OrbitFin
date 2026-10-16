"""Inject OrbitFin design system into Streamlit."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_THEME_PATH = Path(__file__).resolve().parent.parent / "css" / "orbitfin_theme.css"

# Split auth: form esquerda (container) + brand direita — sem absolute / sem overlay
_AUTH_CSS = """
[data-testid="stHeader"],
header[data-testid="stHeader"],
footer,
#MainMenu {
  visibility: hidden !important;
  height: 0 !important;
}
section[data-testid="stSidebar"],
div[data-testid="collapsedControl"] {
  display: none !important;
}

.stApp, [data-testid="stAppViewContainer"], .main {
  background: #FFFFFF !important;
}

.main .block-container {
  max-width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
  min-height: 100vh !important;
}

/* mata gap / footer fantasma do Streamlit na auth */
.stApp, [data-testid="stAppViewContainer"], .main,
[data-testid="stAppViewBlockContainer"] {
  min-height: 100vh !important;
  height: 100% !important;
  overflow-x: hidden !important;
}
[data-testid="stBottomBlockContainer"],
[data-testid="stDecoration"],
footer { display: none !important; height: 0 !important; }

[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container { margin-bottom: 0 !important; }

[data-testid="stHorizontalBlock"] {
  gap: 0 !important;
  min-height: 100vh !important;
  height: 100vh !important;
  align-items: stretch !important;
  margin: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"] {
  padding: 0 !important;
}

/* ——— ESQUERDA ——— */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
  background: #FFFFFF !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div {
  min-height: 100vh !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: stretch !important;
  padding: clamp(2rem, 5vh, 3.5rem) clamp(1.5rem, 4vw, 3.5rem) !important;
  box-sizing: border-box !important;
  max-width: none !important;
}

/* form alinhado no topo, sem “ilha” no meio da coluna */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child
  > div > [data-testid="stVerticalBlock"] {
  width: 100% !important;
  max-width: 400px !important;
  margin: 0 !important;
  gap: 0.25rem !important;
  flex: 1 1 auto !important;
}

.of-auth-logo {
  display: flex !important;
  align-items: center !important;
  gap: 0.6rem !important;
  margin: 0 0 1.75rem !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  color: #010103 !important;
}

.of-auth-logo .of-logo-mark {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: #010103;
  color: #FFF;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

.of-auth-title {
  font-size: 1.65rem !important;
  font-weight: 700 !important;
  color: #010103 !important;
  letter-spacing: -0.03em !important;
  margin: 0 0 0.35rem !important;
  line-height: 1.2 !important;
}

.of-auth-lead {
  font-size: 14px !important;
  color: rgba(25, 25, 25, 0.55) !important;
  margin: 0 0 1.5rem !important;
  line-height: 1.5 !important;
}

.of-auth-switch {
  font-size: 14px !important;
  color: rgba(25, 25, 25, 0.55) !important;
  margin: 1.1rem 0 0.15rem !important;
}

.of-legal {
  font-size: 12px;
  color: rgba(25, 25, 25, 0.45);
  margin-top: 0.35rem;
}

div[data-testid="stTextInput"] label {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #191919 !important;
}

div[data-testid="stTextInput"] input {
  border-radius: 10px !important;
  border: 1px solid rgba(25, 25, 25, 0.14) !important;
  background: #FFF !important;
  min-height: 48px !important;
  font-size: 14px !important;
}

div[data-testid="stTextInput"] input:focus {
  border-color: #010103 !important;
  box-shadow: 0 0 0 1px #010103 !important;
}

.stFormSubmitButton > button,
.stFormSubmitButton button,
button[kind="primaryFormSubmit"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
  width: 100% !important;
  border-radius: 10px !important;
  background: #010103 !important;
  color: #FFFFFF !important;
  border: none !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  min-height: 48px !important;
  margin-top: 0.5rem !important;
  pointer-events: auto !important;
  z-index: 2 !important;
  position: relative !important;
}

.stFormSubmitButton > button:hover {
  background: #191919 !important;
  color: #FFF !important;
  border: none !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child
  .stButton > button {
  background: transparent !important;
  color: #010103 !important;
  border: none !important;
  box-shadow: none !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  text-decoration: underline !important;
  text-underline-offset: 3px !important;
  min-height: auto !important;
  width: auto !important;
  padding: 0.2rem 0 !important;
  pointer-events: auto !important;
}

/* ——— DIREITA (brand) ——— */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
  background: #010103 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) > div {
  min-height: 100vh !important;
  padding: 0 !important;
  max-width: none !important;
}

.of-hero {
  min-height: 100vh;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  padding: clamp(2.5rem, 6vw, 4.5rem);
  display: flex;
  flex-direction: column;
  justify-content: center;
  background:
    radial-gradient(120% 80% at 15% 0%, rgba(243,245,247,0.08) 0%, transparent 50%),
    linear-gradient(165deg, #010103 0%, #191919 55%, #010103 100%);
  color: #FFF;
}

.of-hero-kicker {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  opacity: 0.55;
  margin-bottom: 1.1rem;
}

.of-hero h2 {
  font-size: clamp(1.6rem, 3.2vw, 2.5rem);
  font-weight: 300;
  letter-spacing: -0.03em;
  line-height: 1.15;
  margin: 0 0 1rem;
}

.of-hero p {
  font-size: 14px;
  line-height: 1.65;
  color: rgba(255,255,255,0.7);
  margin: 0;
  max-width: 32ch;
}

.of-hero-badge {
  margin-top: 2rem;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(243,245,247,0.08);
  border: 1px solid rgba(243,245,247,0.12);
  font-size: 24px;
  font-weight: 300;
}

@media (max-width: 900px) {
  [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    min-height: auto !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    min-width: 100% !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child { order: 2 !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { order: 1 !important; }
  [data-testid="stHorizontalBlock"] {
    height: auto !important;
    min-height: auto !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div {
    min-height: auto !important;
    height: auto !important;
    padding: 2rem 1.25rem 2.5rem !important;
  }
  .of-hero {
    min-height: 28vh !important;
    padding: 1.75rem 1.25rem !important;
  }
  div[data-testid="stTextInput"] input { font-size: 16px !important; }
}
"""


_APP_SHELL = """
.stApp, [data-testid="stAppViewContainer"] {
  background: #F3F5F7 !important;
}
.main .block-container {
  padding-top: 0.85rem !important;
  padding-bottom: 1.25rem !important;
  padding-left: 1rem !important;
  padding-right: 1rem !important;
  max-width: none !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}
/* toolbar Streamlit (Share/GitHub) come espaço no topo */
[data-testid="stHeader"],
header[data-testid="stHeader"] {
  background: transparent !important;
  height: 0 !important;
  min-height: 0 !important;
  visibility: hidden !important;
}
[data-testid="stToolbar"] { display: none !important; }

/* Sidebar — coluna flex: brand topo, footer bottom */
section[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  border-right: 1px solid rgba(25,25,25,0.08) !important;
}
section[data-testid="stSidebar"] > div {
  padding-top: 0.65rem !important;
  padding-bottom: 0.65rem !important;
  height: 100% !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"],
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] > div > [data-testid="stVerticalBlock"] {
  height: 100% !important;
  min-height: calc(100vh - 2rem) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 0.15rem !important;
}
.of-side-grow {
  flex: 1 1 auto !important;
  /* fallback se o flex do Streamlit falhar */
  min-height: clamp(2rem, calc(100vh - 420px), 50vh) !important;
  margin: 0 !important;
}
.of-side-footer {
  margin-top: auto !important;
  width: 100%;
  padding-top: 0.5rem;
}
.of-side-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #010103;
  margin: 0 0 1rem;
}
.of-side-mark {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: #010103;
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}
.of-side-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(25,25,25,0.45);
  margin: 0 0 0.75rem;
}
.of-side-user {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.85rem 0.6rem;
  margin-bottom: 0.35rem;
  border-radius: 12px;
  background: #F3F5F7;
}
.of-side-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #FFFFFF;
  color: #010103;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}
.of-side-user-name { font-size: 13px; font-weight: 600; color: #010103; }
.of-side-user-email { font-size: 11px; color: rgba(25,25,25,0.5); word-break: break-all; }

/* Nav ghost — left align */
section[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  border-radius: 8px !important;
  justify-content: flex-start !important;
  text-align: left !important;
  padding: 0.55rem 0.35rem !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  color: #9CA3AF !important;
  gap: 0.55rem !important;
}
section[data-testid="stSidebar"] .stButton > button p,
section[data-testid="stSidebar"] .stButton > button div {
  text-align: left !important;
  justify-content: flex-start !important;
  width: 100% !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  color: #010103 !important;
  background: rgba(1,1,3,0.04) !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: transparent !important;
  color: #010103 !important;
  font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
  background: rgba(1,1,3,0.04) !important;
}
/* Sair um pouco mais forte */
section[data-testid="stSidebar"] button[kind="secondary"][data-testid="stBaseButton-secondary"] {
  font-weight: 600 !important;
  color: #191919 !important;
}

/* Desktop: sidebar sempre aberta, sem seta de collapse */
@media (min-width: 769px) {
  section[data-testid="stSidebar"] {
    transform: none !important;
    visibility: visible !important;
    margin-left: 0 !important;
  }
  [data-testid="collapsedControl"],
  [data-testid="stSidebarCollapsedControl"],
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stExpandSidebarButton"],
  section[data-testid="stSidebar"] [data-testid="stBaseButton-header"],
  section[data-testid="stSidebar"] button[kind="headerNoPadding"],
  section[data-testid="stSidebar"] button[kind="header"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
}

/* Dashboard cards */
.of-page-kicker {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(25,25,25,0.45);
  margin: 0 0 0.25rem;
}
.of-page-title {
  font-size: 1.55rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: #010103;
  margin: 0 0 0.85rem;
}
.of-page-head { margin-bottom: 0.15rem; }

/* CTA preto (mata vermelho default Streamlit Cloud) */
.main .stButton > button[kind="primary"],
.main .stFormSubmitButton > button,
.main button[kind="primaryFormSubmit"],
.main button[data-testid="stBaseButton-primaryFormSubmit"],
.main button[data-testid="stBaseButton-primary"] {
  background: #010103 !important;
  color: #fff !important;
  border: none !important;
}
.of-card {
  background: #FFFFFF;
  border: 1px solid rgba(25,25,25,0.07);
  border-radius: 16px;
  padding: 1.1rem 1.15rem;
  box-shadow: 0 8px 24px rgba(1,1,3,0.03);
}
.of-kpi { min-height: 110px; }
.of-kpi-label {
  font-size: 12px;
  font-weight: 600;
  color: rgba(25,25,25,0.5);
  margin-bottom: 0.45rem;
}
.of-kpi-value {
  font-size: 1.35rem;
  font-weight: 700;
  color: #010103;
  letter-spacing: -0.02em;
}
.of-kpi-hint {
  margin-top: 0.45rem;
  font-size: 12px;
  color: rgba(25,25,25,0.45);
}
.of-kpi-up { color: #16A34A !important; }
.of-kpi-down { color: #EA580C !important; }
.of-card-title {
  font-size: 14px;
  font-weight: 700;
  color: #010103;
  margin: 0 0 0.65rem;
}
.of-gap { height: 1rem; }
.of-empty {
  background: #FFFFFF;
  border: 1px dashed rgba(25,25,25,0.12);
  border-radius: 16px;
  padding: 1.25rem;
  font-size: 14px;
  color: rgba(25,25,25,0.55);
}
.of-insight {
  font-size: 14px;
  line-height: 1.55;
  color: #191919;
  min-height: 88px;
}
.of-budget-row { margin-bottom: 0.85rem; }
.of-budget-row:last-child { margin-bottom: 0; }
.of-budget-top {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #191919;
  margin-bottom: 0.35rem;
  gap: 0.5rem;
}
.of-budget-bar {
  height: 6px;
  background: #F3F5F7;
  border-radius: 999px;
  overflow: hidden;
}
.of-budget-bar > span {
  display: block;
  height: 100%;
  background: #010103;
  border-radius: 999px;
}
.of-tx-list { padding: 0.35rem 1.15rem; }
.of-tx-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(25,25,25,0.06);
}
.of-tx-row:last-child { border-bottom: none; }
.of-tx-cat { font-size: 14px; font-weight: 600; color: #010103; }
.of-tx-meta { font-size: 12px; color: rgba(25,25,25,0.45); margin-top: 0.15rem; }
.of-tx-val { font-size: 14px; font-weight: 700; white-space: nowrap; }
.of-badge-in { color: #16A34A; }
.of-badge-out { color: #EA580C; }

/* Forms / CTAs na área main */
.main .stButton > button[kind="primary"],
.main .stFormSubmitButton > button {
  background: #010103 !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
}
.main .stButton > button[kind="secondary"] {
  background: transparent !important;
  color: #191919 !important;
  border: 1px solid rgba(25,25,25,0.12) !important;
  border-radius: 10px !important;
  font-weight: 500 !important;
}
.main [data-testid="stExpander"] {
  background: #FFFFFF !important;
  border: 1px solid rgba(25,25,25,0.07) !important;
  border-radius: 16px !important;
}
"""


def apply_theme(*, hide_sidebar: bool = False, auth: bool = False) -> None:
    css = _THEME_PATH.read_text(encoding="utf-8")
    if hide_sidebar and not auth:
        css += """
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        """
    if auth:
        css += _AUTH_CSS
    else:
        css += _APP_SHELL
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_config() -> None:
    st.set_page_config(
        page_title="OrbitFin",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="expanded",
    )
