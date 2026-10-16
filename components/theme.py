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
}

[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container { margin-bottom: 0 !important; }

[data-testid="stHorizontalBlock"] {
  gap: 0 !important;
  min-height: 100vh !important;
  align-items: stretch !important;
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
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  align-items: center !important;
  padding: 2.5rem 1.5rem !important;
  box-sizing: border-box !important;
  max-width: none !important;
}

/* container do form (não full-bleed) */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child
  > div > [data-testid="stVerticalBlock"] {
  width: 100% !important;
  max-width: 380px !important;
  margin: 0 auto !important;
  gap: 0.25rem !important;
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
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div {
    min-height: auto !important;
    padding: 2rem 1.25rem 3rem !important;
  }
  .of-hero {
    min-height: 28vh !important;
    padding: 1.75rem 1.25rem !important;
  }
  div[data-testid="stTextInput"] input { font-size: 16px !important; }
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
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_config() -> None:
    st.set_page_config(
        page_title="OrbitFin",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
