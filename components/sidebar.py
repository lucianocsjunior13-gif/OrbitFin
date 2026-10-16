"""Sidebar do app logado — shell estilo APPROX / OrbitFin."""
from __future__ import annotations

import streamlit as st

_NAV = [
    ("dashboard", "Dashboard"),
    ("transacoes", "Transações"),
    ("orcamento", "Orçamento"),
    ("metas", "Metas"),
    ("relatorios", "Relatórios"),
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
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="of-side-label">Menu</p>', unsafe_allow_html=True)

        for key, label in _NAV:
            is_active = current == key
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                if not is_active:
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
            st.rerun()
