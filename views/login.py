"""Tela de Login — design system OrbitFin."""
from __future__ import annotations

import streamlit as st

from services.storage import authenticate_user


def _brand_panel() -> None:
    st.markdown(
        """
        <div class="of-brand">
          <div>
            <div class="of-brand-mark">OrbitFin</div>
            <h1>Controle financeiro sem ruído.</h1>
            <p>Entre para acompanhar saldo, transações e metas em um só lugar.</p>
          </div>
          <div class="of-brand-foot">Finanças pessoais · MVP</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login() -> None:
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        _brand_panel()

    with right:
        st.markdown(
            """
            <div class="of-form-panel">
              <h2>Entrar</h2>
              <p class="of-sub">Use o e-mail e a senha da sua conta OrbitFin.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("E-mail", placeholder="voce@email.com", key="login_email")
            password = st.text_input(
                "Senha", type="password", placeholder="••••••••", key="login_password"
            )
            submitted = st.form_submit_button("Entrar")

        if submitted:
            if not email or not password:
                st.error("Preencha e-mail e senha.")
            else:
                user = authenticate_user(email.strip(), password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos.")

        st.markdown('<p class="of-switch">Ainda não tem conta?</p>', unsafe_allow_html=True)
        if st.button("Criar conta", type="secondary", use_container_width=True):
            st.session_state.auth_page = "register"
            st.rerun()
