"""Header das páginas do app logado — só título (sem busca fantasma)."""
from __future__ import annotations

import streamlit as st

_TITLES = {
    "dashboard": ("Visão geral", "Dashboard"),
    "transacoes": ("Movimentações", "Transações"),
    "orcamento": ("Planejamento", "Orçamento"),
    "metas": ("Planejamento", "Metas"),
    "relatorios": ("Análises", "Relatórios"),
}


def render_header(page: str | None = None) -> None:
    page = page or st.session_state.get("page", "dashboard")
    kicker, title = _TITLES.get(page, ("OrbitFin", page.title()))
    st.markdown(
        f'<div class="of-page-head"><p class="of-page-kicker">{kicker}</p>'
        f'<h1 class="of-page-title">{title}</h1></div>',
        unsafe_allow_html=True,
    )
