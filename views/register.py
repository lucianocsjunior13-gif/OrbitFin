"""Tela de Registro — design system OrbitFin."""
from __future__ import annotations

import streamlit as st

from services.storage import create_user


def _brand_panel() -> None:
    st.markdown(
        """
        <div class="of-brand">
          <div>
            <div class="of-brand-mark">OrbitFin</div>
            <h1>Comece a organizar seu dinheiro.</h1>
            <p>Cadastro rápido. Seus dados ficam na conta — login seguro via Xano.</p>
          </div>
          <div class="of-brand-foot">Senha: mín. 8 caracteres, 1 letra e 1 número</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_register() -> None:
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        _brand_panel()

    with right:
        st.markdown(
            """
            <div class="of-form-panel">
              <h2>Criar conta</h2>
              <p class="of-sub">Preencha os campos para criar seu acesso.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("register_form", clear_on_submit=False):
            name = st.text_input("Nome completo", placeholder="Seu nome", key="reg_name")
            email = st.text_input("E-mail", placeholder="voce@email.com", key="reg_email")
            password = st.text_input(
                "Senha", type="password", placeholder="Mín. 8 caracteres", key="reg_password"
            )
            confirm = st.text_input(
                "Confirmar senha", type="password", placeholder="Repita a senha", key="reg_confirm"
            )
            submitted = st.form_submit_button("Criar conta")

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
                    st.success(f"Conta criada. Bem-vindo(a), {user['name']}!")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Erro ao criar conta: {e}")

        st.markdown('<p class="of-switch">Já tem conta?</p>', unsafe_allow_html=True)
        if st.button("Fazer login", type="secondary", use_container_width=True):
            st.session_state.auth_page = "login"
            st.rerun()
