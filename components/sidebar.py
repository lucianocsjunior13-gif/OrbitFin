"""Sidebar — links texto + ícones Lucide (SVG), sem pills."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

_ICONS = {
    "dashboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
    "transacoes": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/></svg>',
    "orcamento": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>',
    "metas": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "relatorios": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
}

_NAV = [
    ("dashboard", "Dashboard"),
    ("transacoes", "Transações"),
    ("orcamento", "Orçamento"),
    ("metas", "Metas"),
    ("relatorios", "Relatórios"),
]

_NAV_KEYS = {k for k, _ in _NAV}


def sync_nav_from_query() -> None:
    """Lê ?nav= da URL (links HTML da sidebar)."""
    try:
        nav = st.query_params.get("nav")
    except Exception:
        nav = None
    if nav in _NAV_KEYS:
        st.session_state.page = nav


def render_sidebar() -> None:
    sync_nav_from_query()

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

        # iframe: Streamlit sanitize remove <svg> do markdown
        links = []
        for key, label in _NAV:
            active = "is-active" if current == key else ""
            links.append(
                f'<a class="of-nav-link {active}" href="?nav={key}" target="_parent">'
                f'<span class="of-nav-ico">{_ICONS[key]}</span>'
                f"<span>{label}</span></a>"
            )
        nav_html = f"""
        <style>
          html,body{{margin:0;padding:0;background:transparent;
            font-family:Manrope,system-ui,sans-serif;}}
          .of-nav{{display:flex;flex-direction:column;gap:2px;}}
          .of-nav-link{{
            display:flex;align-items:center;gap:11px;
            padding:9px 7px;border-radius:8px;text-decoration:none;
            color:#9CA3AF;font-size:14px;font-weight:500;
          }}
          .of-nav-link:hover{{color:#010103;}}
          .of-nav-link.is-active{{color:#010103;font-weight:700;}}
          .of-nav-ico{{width:18px;height:18px;display:inline-flex;flex-shrink:0;}}
          .of-nav-ico svg{{width:18px;height:18px;display:block;}}
        </style>
        <nav class="of-nav">{"".join(links)}</nav>
        """
        components.html(nav_html, height=220, scrolling=False)

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
