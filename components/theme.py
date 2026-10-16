"""Inject OrbitFin design system into Streamlit."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_THEME_PATH = Path(__file__).resolve().parent.parent / "css" / "orbitfin_theme.css"

# CSS nuclear: Streamlit Cloud injeta padding enorme no .block-container
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
  min-height: 100vh !important;
  background: #FFFFFF !important;
  overflow: hidden !important;
}

[data-testid="stHeader"],
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
  display: none !important;
  height: 0 !important;
  visibility: hidden !important;
}

section[data-testid="stSidebar"],
div[data-testid="collapsedControl"] {
  display: none !important;
}

/* mata o padding absurdo do Streamlit */
.main .block-container,
div.block-container,
.stMainBlockContainer,
[data-testid="stMainBlockContainer"],
.block-container {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
  margin: 0 !important;
  min-height: 100vh !important;
  height: 100vh !important;
}

/* remove gaps verticais do Streamlit entre elementos */
[data-testid="stVerticalBlock"] {
  gap: 0 !important;
}
[data-testid="stVerticalBlock"] > div {
  gap: 0 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
  border: none !important;
}
.element-container,
div[data-testid="element-container"] {
  margin: 0 !important;
  padding: 0 !important;
}

/* row 50/50 grudada nas bordas */
[data-testid="stHorizontalBlock"] {
  gap: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100vh !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
  align-items: stretch !important;
  display: flex !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"] {
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
}

/* coluna form — padding INTERNO só (conteúdo, não a página) */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
  background: #FFFFFF !important;
  padding: 2.5rem 3.5rem !important;
  overflow-y: auto !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}

/* coluna hero — preto até a borda */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
  background: #010103 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2)
  [data-testid="stMarkdownContainer"],
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2)
  [data-testid="stMarkdown"],
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) > div {
  height: 100% !important;
  min-height: 100vh !important;
}

.of-hero {
  min-height: 100vh !important;
  height: 100vh !important;
  width: 100% !important;
  margin: 0 !important;
  border-radius: 0 !important;
  box-sizing: border-box !important;
}

/* botão primário do form */
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
.stFormSubmitButton > button:hover {
  background: #191919 !important;
  color: #FFFFFF !important;
  border: none !important;
}

/* link "Criar conta" — nunca pill branca */
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
  height: auto !important;
  padding: 0 !important;
  width: auto !important;
  border-radius: 0 !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child
  .stButton > button:hover {
  background: transparent !important;
  color: #191919 !important;
  border: none !important;
}

@media (max-width: 900px) {
  html, body, .stApp, .main, .block-container {
    height: auto !important;
    max-height: none !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
  }
  [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    flex-wrap: wrap !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    flex: 1 1 100% !important;
    min-width: 100% !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
    order: 2 !important;
    padding: 1.5rem 1.25rem 2rem !important;
    justify-content: flex-start !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {
    order: 1 !important;
    min-height: 28vh !important;
  }
  .of-hero {
    min-height: 28vh !important;
    height: 28vh !important;
    padding: 1.5rem 1.25rem !important;
  }
  div[data-testid="stTextInput"] input {
    font-size: 16px !important;
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
