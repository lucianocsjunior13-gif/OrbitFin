"""Tela de Registro — full-bleed (form | hero)."""
from __future__ import annotations

import streamlit as st

from services.storage import create_user


def render_register() -> None:
    form_col, hero_col = st.columns(2, gap="small")

    with form_col:
        st.markdown(
            """
            <div class="of-logo"><span class="of-logo-mark">O</span> OrbitFin</div>
            <p class="of-title">Crie sua conta</p>
            <p class="of-lead">Preencha os dados para começar a organizar suas finanças.</p>
            """,
            unsafe_allow_html=True,
        )

        with st.form("register_form", clear_on_submit=False, border=False):
            name = st.text_input("Nome completo", placeholder="Seu nome", key="reg_name")
            email = st.text_input("E-mail", placeholder="voce@email.com", key="reg_email")
            password = st.text_input(
                "Senha",
                type="password",
                placeholder="Mín. 8 caracteres, 1 letra e 1 número",
                key="reg_password",
            )
            confirm = st.text_input(
                "Confirmar senha",
                type="password",
                placeholder="Repita a senha",
                key="reg_confirm",
            )
            submitted = st.form_submit_button("Criar conta", use_container_width=True)

        if submitted:
            if password != confirm:
                st.error("As senhas não coincidem.")
            elif not name or not email or not password:
                st.error("Preencha todos os campos.")
            else:
                try:
                    user = create_user(email.strip(), password, name.strip())
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Erro ao criar conta: {e}")

        st.markdown(
            '<p class="of-legal">Senha: mínimo 8 caracteres, com pelo menos 1 letra e 1 número.</p>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 1.2])
        with c1:
            st.markdown(
                '<p class="of-switch-inline">Já tem conta?</p>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown('<div class="of-linkish"></div>', unsafe_allow_html=True)
            if st.button("Fazer login", key="go_login"):
                st.session_state.auth_page = "login"
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
                <h2>Comece a organizar seu dinheiro.</h2>
                <p>Cadastro rápido, login seguro e orçamentos prontos para acompanhar o mês.</p>
                <div class="of-hero-badge">OF</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
