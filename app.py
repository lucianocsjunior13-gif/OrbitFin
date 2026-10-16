import streamlit as st

from components.theme import page_config, apply_theme
from components.sidebar import render_sidebar
from components.header import render_header
from views.login import render_login
from views.register import render_register
from views.dashboard import render_dashboard
from views.transactions import render_transactions
from views.budget import render_budget
from views.goals import render_goals
from views.reports import render_reports

page_config()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = "login"

def main_app():
    """Main application after login."""
    apply_theme(hide_sidebar=False, auth=False)
    render_sidebar()

    if st.session_state.page == "dashboard":
        render_dashboard()
    elif st.session_state.page == "transacoes":
        render_header("transacoes")
        render_transactions()
    elif st.session_state.page == "orcamento":
        render_header("orcamento")
        render_budget()
    elif st.session_state.page == "metas":
        render_header("metas")
        render_goals()
    elif st.session_state.page == "relatorios":
        render_header("relatorios")
        render_reports()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        apply_theme(hide_sidebar=True, auth=True)
        if st.session_state.auth_page == "register":
            render_register()
        else:
            render_login()
    else:
        main_app()