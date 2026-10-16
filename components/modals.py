"""Modais OrbitFin via st.dialog (Streamlit ≥1.33)."""
from __future__ import annotations

from typing import Any, Callable

import streamlit as st

_HAS_DIALOG = hasattr(st, "dialog")


def confirm_action(
    *,
    title: str,
    body: str,
    confirm_label: str = "Confirmar",
    cancel_label: str = "Cancelar",
    destructive: bool = True,
    on_confirm: Callable[[], Any],
) -> None:
    """Abra no mesmo run do clique (ex.: Excluir). Cancelar só fecha o modal."""

    if _HAS_DIALOG:

        @st.dialog(title)
        def _dlg() -> None:
            st.markdown(body)
            c1, c2 = st.columns(2)
            with c1:
                if st.button(
                    confirm_label,
                    type="primary" if destructive else "secondary",
                    use_container_width=True,
                    key="of_modal_confirm",
                ):
                    on_confirm()
                    st.rerun()
            with c2:
                if st.button(cancel_label, use_container_width=True, key="of_modal_cancel"):
                    st.rerun()

        _dlg()
        return

    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(body)
        c1, c2 = st.columns(2)
        with c1:
            if st.button(confirm_label, type="primary", use_container_width=True, key="of_modal_confirm_fb"):
                on_confirm()
                st.rerun()
        with c2:
            if st.button(cancel_label, use_container_width=True, key="of_modal_cancel_fb"):
                st.rerun()
