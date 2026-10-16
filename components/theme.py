"""Inject OrbitFin design system into Streamlit."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_THEME_PATH = Path(__file__).resolve().parent.parent / "css" / "orbitfin_theme.css"

_AUTH_FULLBLEED = """
html, body {
  margin: 0 !important;
  padding: 0 !important;
  height: 100% !important;
  overflow: hidden !important;
  background: #FFFFFF !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
section.main,
.main {
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh !important;
  max-height: 100vh !important;
  background: #FFFFFF !important;
  overflow: hidden !important;
}

[data-testid="stHeader"],
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
footer {
  display: none !important;
  height: 0 !important;
}

section[data-testid="stSidebar"],
div[data-testid="collapsedControl"] {
  display: none !important;
}

.main .block-container,
div.block-container,
.stMainBlockContainer,
[data-testid="stMainBlockContainer"] {
  max-width: 100% !important;
  width: 100% !important;
  height: 100vh !important;
  max-height: 100vh !important;
  padding: 0 !important;
  margin: 0 !important;
  overflow: hidden !important;
}

/* um único bloco vertical = a row split */
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlock"] {
  gap: 0 !important;
  height: 100vh !important;
  max-height: 100vh !important;
  overflow: hidden !important;
}

.element-container,
div[data-testid="element-container"] {
  margin: 0 !important;
}

[data-testid="stHorizontalBlock"] {
  gap: 0 !important;
  margin: 0 !important;
  width: 100% !important;
  height: 100vh !important;
  max-height: 100vh !important;
  align-items: stretch !important;
  display: flex !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"] {
  margin: 0 !important;
  height: 100vh !important;
  max-height: 100vh !important;
  overflow: hidden !important;
}

/* ——— ESQUERDA: logo topo + form centro ——— */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
  background: #FFFFFF !important;
  padding: 0 !important;
  position: relative !important;
  box-sizing: border-box !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div {
  height: 100vh !important;
  max-height: 100vh !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 5.5rem 3.5rem 2.5rem 3.5rem !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
}

.of-logo {
  position: absolute !important;
  top: 1.75rem !important;
  left: 2rem !important;
  z-index: 5 !important;
  margin: 0 !important;
}

.of-form-block {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.of-switch-line {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 0.5rem !important;
  flex-wrap: nowrap !important;
  margin-top: 1rem !important;
  font-size: 14px !important;
  color: rgba(25, 25, 25, 0.55) !important;
  white-space: nowrap !important;
}

.of-switch-line span {
  white-space: nowrap !important;
}

/* ——— DIREITA: hero full ——— */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
  background: #010103 !important;
  padding: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) > div {
  height: 100vh !important;
  max-height: 100vh !important;
  padding: 0 !important;
  margin: 0 !important;
  max-width: none !important;
}

.of-hero {
  height: 100vh !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
  width: 100% !important;
  margin: 0 !important;
  border-radius: 0 !important;
  display: flex !important;
  align-items: center !important;
  box-sizing: border-box !important;
}

/* botão submit */
.stFormSubmitButton > button,
.stFormSubmitButton button,
button[kind="primaryFormSubmit"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
  width: 100% !important;
  border-radius: 12px !important;
  background: #010103 !important;
  color: #FFFFFF !important;
  border: none !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  min-height: 52px !important;
  margin-top: 0.75rem !important;
}

/* botão "Criar conta" vira link inline */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stButton > button {
  background: transparent !important;
  color: #010103 !important;
  border: none !important;
  box-shadow: none !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  text-decoration: underline !important;
  text-underline-offset: 3px !important;
  min-height: auto !important;
  height: auto !important;
  padding: 0 !important;
  width: auto !important;
  border-radius: 0 !important;
  margin: 0 !important;
}

@media (max-width: 900px) {
  html, body, .stApp, .main, .block-container,
  [data-testid="stVerticalBlock"],
  [data-testid="stHorizontalBlock"],
  [data-testid="stHorizontalBlock"] > [data-testid="column"],
  [data-testid="stHorizontalBlock"] > [data-testid="column"] > div {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
  }
  body, .stApp, .main { overflow-y: auto !important; }
  [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    min-width: 100% !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child { order: 2 !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) { order: 1 !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child > div {
    padding: 4.5rem 1.5rem 2rem !important;
    justify-content: flex-start !important;
  }
  .of-logo { top: 1.25rem !important; left: 1.25rem !important; }
  .of-hero {
    height: 30vh !important;
    min-height: 30vh !important;
    max-height: 30vh !important;
    padding: 1.5rem !important;
  }
  .of-switch-line { white-space: normal !important; flex-wrap: wrap !important; }
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
        css += _AUTH_FULLBLEED
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_config() -> None:
    st.set_page_config(
        page_title="OrbitFin",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
