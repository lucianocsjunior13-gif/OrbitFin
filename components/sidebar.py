"""Sidebar — botões ghost + ícones (nav confiável no Streamlit)."""
from __future__ import annotations

import streamlit as st

# Material Symbols (nativo Streamlit ≥1.39) — sem iframe / query params
_NAV = [
    ("dashboard", "Dashboard", ":material/dashboard:"),
    ("transacoes", "Transações", ":material/swap_horiz:"),
    ("orcamento", "Orçamento", ":material/account_balance_wallet:"),
    ("metas", "Metas", ":material/track_changes:"),
    ("relatorios", "Relatórios", ":material/bar_chart:"),
]


def render_sidebar() -> None:
    user = st.session_state.user or {}
    name = user.get("name") or "Usuário"
    email = user.get("email") or ""
    initial = (name[:1] or "U").upper()
    current = st.session_state.get("page", "dashboard")

    with st.sidebar:
        st.markdown(
            """
            <div class="of-side-brand">
              <span class="of-side-mark">O</span>
              <span>OrbitFin</span>
            </div>
            <p class="of-side-label">Menu</p>
            """,
            unsafe_allow_html=True,
        )

        for key, label, icon in _NAV:
            active = current == key
            # type primary no ativo só pra contraste tipográfico via CSS ghost
            clicked = st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary",
            )
            if clicked and not active:
                st.session_state.page = key
                st.rerun()

        st.markdown('<div class="of-side-spacer"></div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="of-side-user">
              <div class="of-side-avatar">{initial}</div>
              <div>
                <div class="of-side-user-name">{name}</div>
                <div class="of-side-user-email">{email}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sair", key="logout_btn", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.token = None
            st.session_state.auth_page = "login"
            st.session_state.page = "dashboard"
            try:
                st.query_params.clear()
            except Exception:
                pass
            st.rerun()
