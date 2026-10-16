"""Header das páginas do app logado."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

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

    # SVG no markdown some no bleach — header visual via iframe
    topbar = """
    <style>
      body{margin:0;font-family:Manrope,system-ui,sans-serif;background:transparent}
      .of-topbar{display:flex;align-items:center;justify-content:space-between;gap:1rem}
      .of-search{display:flex;align-items:center;gap:.55rem;background:#fff;
        border:1px solid rgba(25,25,25,.08);border-radius:999px;padding:.65rem 1rem;
        flex:1;max-width:420px;color:rgba(25,25,25,.45);font-size:13px}
      .of-search-ico{display:inline-flex;color:#191919}
      .of-top-actions{display:flex;gap:.5rem}
      .of-icon-btn{width:40px;height:40px;border-radius:50%;background:#fff;
        border:1px solid rgba(25,25,25,.08);display:inline-flex;align-items:center;
        justify-content:center;color:#191919}
    </style>
    <div class="of-topbar">
      <div class="of-search">
        <span class="of-search-ico" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </span>
        <span>Buscar...</span>
      </div>
      <div class="of-top-actions">
        <span class="of-icon-btn" title="Notificações">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
        </span>
        <span class="of-icon-btn" title="Mensagens">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
        </span>
      </div>
    </div>
    """
    components.html(topbar, height=56, scrolling=False)
    st.markdown(
        f'<div class="of-page-head"><p class="of-page-kicker">{kicker}</p>'
        f'<h1 class="of-page-title">{title}</h1></div>',
        unsafe_allow_html=True,
    )
