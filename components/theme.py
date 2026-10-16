"""Inject OrbitFin design system into Streamlit."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_THEME_PATH = Path(__file__).resolve().parent.parent / "css" / "orbitfin_theme.css"

# Auth simples: form centralizado (estilo referência Logoipsum)
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

/* form centralizado na viewport (container, não full-bleed) */
.main .block-container {
  max-width: 440px !important;
  padding-top: min(12vh, 6rem) !important;
  padding-bottom: 3rem !important;
  padding-left: 1.5rem !important;
  padding-right: 1.5rem !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

[data-testid="stVerticalBlock"] {
  gap: 0.35rem !important;
}

.of-auth-logo {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.65rem !important;
  margin: 0 0 2rem !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  color: #010103 !important;
}

.of-auth-logo .of-logo-mark {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #010103;
  color: #FFFFFF;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.of-auth-title {
  text-align: center !important;
  font-size: 1.75rem !important;
  font-weight: 700 !important;
  color: #010103 !important;
  letter-spacing: -0.03em !important;
  margin: 0 0 0.4rem !important;
  line-height: 1.2 !important;
}

.of-auth-lead {
  text-align: center !important;
  font-size: 14px !important;
  color: rgba(25, 25, 25, 0.55) !important;
  margin: 0 0 1.75rem !important;
  line-height: 1.5 !important;
}

.of-auth-switch {
  text-align: center !important;
  font-size: 14px !important;
  color: rgba(25, 25, 25, 0.55) !important;
  margin: 1.25rem 0 0.25rem !important;
}

div[data-testid="stTextInput"] label {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #191919 !important;
}

div[data-testid="stTextInput"] input {
  border-radius: 10px !important;
  border: 1px solid rgba(25, 25, 25, 0.14) !important;
  background: #FFFFFF !important;
  min-height: 48px !important;
  font-size: 14px !important;
}

div[data-testid="stTextInput"] input:focus {
  border-color: #010103 !important;
  box-shadow: 0 0 0 1px #010103 !important;
}

/* botão primário do form — SEM overlay, SEM pointer-events bloqueado */
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
  position: relative !important;
  z-index: 2 !important;
}

.stFormSubmitButton > button:hover {
  background: #191919 !important;
  color: #FFFFFF !important;
  border: none !important;
}

/* link "Criar conta" */
.main .block-container .stButton > button {
  background: transparent !important;
  color: #010103 !important;
  border: none !important;
  box-shadow: none !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  text-decoration: underline !important;
  text-underline-offset: 3px !important;
  min-height: auto !important;
  width: 100% !important;
  padding: 0.25rem !important;
  pointer-events: auto !important;
}

.of-legal {
  text-align: center;
  font-size: 12px;
  color: rgba(25, 25, 25, 0.45);
  margin-top: 0.5rem;
}

@media (max-width: 480px) {
  .main .block-container {
    padding: 2rem 1.25rem 3rem !important;
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
        css += _AUTH_CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_config() -> None:
    # wide no app; auth limita largura via CSS (.block-container max-width)
    st.set_page_config(
        page_title="OrbitFin",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
