"""
Storage remoto via Xano — mesma interface pública de sqlite_storage.
OpenSpec 002 / Fase 7.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime

import streamlit as st

from services.api_client import login, register, api_get, api_post, api_put, api_delete


def _as_list(data: Any) -> List[Dict[str, Any]]:
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "items" in data:
        return data["items"] or []
    return []


def _user_from_auth(data: Dict[str, Any]) -> Dict[str, Any]:
    token = data.get("access_token")
    if not token:
        raise ValueError("Resposta do Xano sem access_token")
    st.session_state.token = token
    return {
        "id": data.get("user_id"),
        "name": data.get("name") or "",
        "email": data.get("email") or "",
    }


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    try:
        data = login(email, password)
        return _user_from_auth(data)
    except Exception:
        return None


def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    try:
        data = register(email, password, name)
        return _user_from_auth(data)
    except Exception as e:
        raise ValueError(str(e)) from e


def get_transactions(user_id: int) -> List[Dict[str, Any]]:
    # user_id vem do app; no Xano o filtro é pelo Bearer ($auth.id)
    return _as_list(api_get("/transacoes"))


def add_transaction(user_id: int, transaction_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    payload = {
        "tipo": transaction_data.get("tipo"),
        "valor": float(transaction_data.get("valor", 0)),
        "data": transaction_data.get("data"),
        "categoria": transaction_data.get("categoria", ""),
        "descricao": transaction_data.get("descricao") or "",
        "status": transaction_data.get("status", "pago"),
    }
    return api_post("/transacoes", payload)


def update_transaction(
    user_id: int, transaction_id: int, transaction_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    payload = {
        "tipo": transaction_data.get("tipo"),
        "valor": float(transaction_data.get("valor", 0)),
        "data": transaction_data.get("data"),
        "categoria": transaction_data.get("categoria", ""),
        "descricao": transaction_data.get("descricao") or "",
        "status": transaction_data.get("status", "pago"),
    }
    return api_put(f"/transacoes/{transaction_id}", payload)


def delete_transaction(user_id: int, transaction_id: int) -> bool:
    return api_delete(f"/transacoes/{transaction_id}")


def get_budgets() -> List[Dict[str, Any]]:
    return _as_list(api_get("/budgets"))


def update_budget(budget_id: int, limite: float) -> Optional[Dict[str, Any]]:
    # Endpoint PUT /budgets/{id} ainda não existe no Xano (Fase 4 mínima)
    st.warning("Atualizar budget no Xano ainda não está disponível. Crie o endpoint depois.")
    return None


def get_insights() -> Dict[str, Any]:
    data = api_get("/insights")
    if isinstance(data, dict) and "texto" in data:
        return data
    return {"texto": "Nenhum insight disponivel ainda."}


def update_insights(texto: str) -> Dict[str, Any]:
    st.warning("Atualizar insight no Xano ainda não está disponível.")
    return get_insights()


def get_expenses_by_category(user_id: int) -> Dict[str, float]:
    result: Dict[str, float] = {}
    for t in get_transactions(user_id):
        if t.get("tipo") != "despesa":
            continue
        cat = t.get("categoria") or "Outros"
        result[cat] = result.get(cat, 0.0) + float(t.get("valor") or 0)
    return result


def get_income_by_category(user_id: int) -> Dict[str, float]:
    result: Dict[str, float] = {}
    for t in get_transactions(user_id):
        if t.get("tipo") != "receita":
            continue
        cat = t.get("categoria") or "Outros"
        result[cat] = result.get(cat, 0.0) + float(t.get("valor") or 0)
    return result


def get_monthly_summary(user_id: int, year: int, month: int) -> Dict[str, Any]:
    receitas = 0.0
    despesas = 0.0
    by_cat_desp: Dict[str, float] = {}
    by_cat_rec: Dict[str, float] = {}

    for t in get_transactions(user_id):
        data = str(t.get("data") or "")
        try:
            dt = datetime.fromisoformat(data[:10])
        except ValueError:
            continue
        if dt.year != year or dt.month != month:
            continue
        valor = float(t.get("valor") or 0)
        cat = t.get("categoria") or "Outros"
        if t.get("tipo") == "receita":
            receitas += valor
            by_cat_rec[cat] = by_cat_rec.get(cat, 0.0) + valor
        elif t.get("tipo") == "despesa":
            despesas += valor
            by_cat_desp[cat] = by_cat_desp.get(cat, 0.0) + valor

    return {
        "total_receitas": receitas,
        "total_despesas": despesas,
        "balance": receitas - despesas,
        "expenses_by_category": [
            {"categoria": k, "total": v} for k, v in by_cat_desp.items()
        ],
        "income_by_category": [
            {"categoria": k, "total": v} for k, v in by_cat_rec.items()
        ],
    }


def get_yearly_summary(user_id: int, year: int) -> Dict[str, Any]:
    receitas = 0.0
    despesas = 0.0
    by_month: Dict[int, Dict[str, float]] = {
        m: {"receitas": 0.0, "despesas": 0.0} for m in range(1, 13)
    }

    for t in get_transactions(user_id):
        data = str(t.get("data") or "")
        try:
            dt = datetime.fromisoformat(data[:10])
        except ValueError:
            continue
        if dt.year != year:
            continue
        valor = float(t.get("valor") or 0)
        if t.get("tipo") == "receita":
            receitas += valor
            by_month[dt.month]["receitas"] += valor
        elif t.get("tipo") == "despesa":
            despesas += valor
            by_month[dt.month]["despesas"] += valor

    monthly_data = []
    for m in range(1, 13):
        r = by_month[m]["receitas"]
        d = by_month[m]["despesas"]
        if r or d:
            monthly_data.append(
                {
                    "month": f"{m:02d}",
                    "receitas": r,
                    "despesas": d,
                    "balance": r - d,
                }
            )

    return {
        "total_receitas": receitas,
        "total_despesas": despesas,
        "balance": receitas - despesas,
        "monthly_data": monthly_data,
    }
