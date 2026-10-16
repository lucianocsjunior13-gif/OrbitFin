"""Tela de Login — form centralizado (referência Logoipsum)."""
from __future__ import annotations

import streamlit as st

from services.storage import authenticate_user


def render_login() -> None:
    st.markdown(
        """
        <div class="of-auth-logo">
          <span class="of-logo-mark">O</span>
          <span>OrbitFin</span>
        </div>
        <p class="of-auth-title">Bem-vindo de volta</p>
        <p class="of-auth-lead">Entre para gerenciar saldo, transações e metas com clareza.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False, border=False):
        email = st.text_input("E-mail", placeholder="voce@email.com", key="login_email")
        password = st.text_input(
            "Senha", type="password", placeholder="Digite sua senha", key="login_password"
        )
        submitted = st.form_submit_button("Entrar", use_container_width=True)

    if submitted:
        if not email or not password:
            st.error("Preencha e-mail e senha.")
        else:
            try:
                user = authenticate_user(email.strip(), password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    st.session_state.auth_page = "login"
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos.")
            except Exception as e:
                st.error(f"Erro ao entrar: {e}")

    st.markdown(
        '<p class="of-auth-switch">Ainda não tem uma conta?</p>',
        unsafe_allow_html=True,
    )
    if st.button("Criar conta", key="go_register", use_container_width=True):
        st.session_state.auth_page = "register"
        st.rerun()
