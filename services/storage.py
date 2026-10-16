"""
Adapter OpenSpec 002 — escolhe SQLite local ou Xano.

Flag em .streamlit/secrets.toml:
  [xano]
  enabled = true
  base_url = "https://..../api:orbitfin"
"""
from __future__ import annotations


def _use_xano() -> bool:
    try:
        import streamlit as st

        xano = st.secrets.get("xano", {})
        return bool(xano.get("enabled", False)) and bool(xano.get("base_url"))
    except Exception:
        return False


if _use_xano():
    from services.xano_storage import (  # noqa: F401
        authenticate_user,
        create_user,
        get_transactions,
        add_transaction,
        update_transaction,
        delete_transaction,
        get_budgets,
        update_budget,
        get_insights,
        update_insights,
        get_expenses_by_category,
        get_income_by_category,
        get_monthly_summary,
        get_yearly_summary,
    )
else:
    from services.sqlite_storage import (  # noqa: F401
        authenticate_user,
        create_user,
        get_transactions,
        add_transaction,
        update_transaction,
        delete_transaction,
        get_budgets,
        update_budget,
        get_insights,
        update_insights,
        get_expenses_by_category,
        get_income_by_category,
        get_monthly_summary,
        get_yearly_summary,
    )
