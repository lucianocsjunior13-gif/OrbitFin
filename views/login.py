"""Tela de Login — full-bleed (form | hero)."""
from __future__ import annotations

import streamlit as st

from services.storage import authenticate_user


def render_login() -> None:
    form_col, hero_col = st.columns(2, gap="small")

    with form_col:
        st.markdown(
            """
            <div class="of-logo"><span class="of-logo-mark">O</span> OrbitFin</div>
            <p class="of-title">Bem-vindo de volta</p>
            <p class="of-lead">Entre para gerenciar saldo, transações e metas com clareza.</p>
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
                user = authenticate_user(email.strip(), password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos.")

        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.markdown(
                '<p class="of-switch-inline">Ainda não tem conta?</p>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown('<div class="of-linkish"></div>', unsafe_allow_html=True)
            if st.button("Criar conta", key="go_register"):
                st.session_state.auth_page = "register"
                st.rerun()

        st.markdown(
            '<p class="of-footer-mini">© OrbitFin · Finanças pessoais</p>',
            unsafe_allow_html=True,
        )

    with hero_col:
        st.markdown(
            """
            <div class="of-hero">
              <div class="of-hero-inner">
                <div class="of-hero-kicker">OrbitFin</div>
                <h2>Controle financeiro sem ruído.</h2>
                <p>Uma visão clara do seu dinheiro — receitas, despesas e limites por categoria em um só lugar.</p>
                <div class="of-hero-badge">OF</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
