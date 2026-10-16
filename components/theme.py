"""Inject OrbitFin design system into Streamlit."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_THEME_PATH = Path(__file__).resolve().parent.parent / "css" / "orbitfin_theme.css"

_AUTH_FULLBLEED = """
/* Auth full-bleed — só injetado nas telas de login/registro */
.stApp, [data-testid="stAppViewContainer"] {
  background: #FFFFFF !important;
}
.main .block-container {
  max-width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}
[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
div[data-testid="collapsedControl"] { display: none !important; }

[data-testid="stHorizontalBlock"] {
  gap: 0 !important;
  min-height: 100vh !important;
  align-items: stretch !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
  background: #FFFFFF !important;
  padding: clamp(2rem, 5vw, 4.5rem) clamp(1.5rem, 5vw, 5rem) !important;
  min-height: 100vh !important;
  box-sizing: border-box !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
  padding: 0 !important;
  background: #010103 !important;
  min-height: 100vh !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) [data-testid="stMarkdownContainer"] {
  height: 100%;
}

.stFormSubmitButton > button,
.stFormSubmitButton button {
  width: 100% !important;
  border-radius: 12px !important;
  background: #010103 !important;
  color: #FFFFFF !important;
  border: none !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  min-height: 52px !important;
  margin-top: 0.5rem !important;
}
.stFormSubmitButton > button:hover {
  background: #191919 !important;
  color: #FFFFFF !important;
  border: none !important;
}

/* "Criar conta" / "Fazer login" como link */
.of-linkish + div .stButton > button,
[data-testid="stHorizontalBlock"] [data-testid="column"] .stButton > button {
  background: transparent !important;
  color: #010103 !important;
  border: none !important;
  box-shadow: none !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  text-decoration: underline;
  text-underline-offset: 3px;
  min-height: auto !important;
  padding: 0.25rem 0 !important;
  width: auto !important;
  border-radius: 0 !important;
}
.of-linkish + div .stButton > button:hover {
  color: #191919 !important;
  background: transparent !important;
  border: none !important;
}

@media (max-width: 900px) {
  [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    flex-wrap: wrap !important;
    min-height: auto !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    flex: 1 1 100% !important;
    min-width: 100% !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
    min-height: auto !important;
    padding: 1.75rem 1.25rem 2rem !important;
    order: 2 !important; /* form embaixo no mobile */
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
    min-height: 32vh !important;
    order: 1 !important; /* brand no topo */
  }
  .of-hero {
    min-height: 32vh !important;
    padding: 1.75rem 1.25rem !important;
  }
  .of-hero h2 {
    font-size: 1.5rem !important;
  }
  .of-hero-badge {
    width: 64px !important;
    height: 64px !important;
    font-size: 20px !important;
    margin-top: 1.25rem !important;
  }
  .of-title {
    font-size: 1.6rem !important;
  }
  div[data-testid="stTextInput"] input {
    min-height: 48px !important;
    font-size: 16px !important; /* evita zoom iOS */
  }
  .stFormSubmitButton > button {
    min-height: 48px !important;
  }
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
        css += _AUTH_FULLBLEED
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_config() -> None:
    st.set_page_config(
        page_title="OrbitFin",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
