"""Inject OrbitFin design system into Streamlit."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_THEME_PATH = Path(__file__).resolve().parent.parent / "css" / "orbitfin_theme.css"


def apply_theme(*, hide_sidebar: bool = False) -> None:
    css = _THEME_PATH.read_text(encoding="utf-8")
    if hide_sidebar:
        css += """
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_config() -> None:
    st.set_page_config(
        page_title="OrbitFin",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
