"""Dashboard redesenhado — KPIs + chart + insight (ref. APPROX)."""
from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.storage import get_budgets, get_insights, get_transactions


def _money(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _kpi(label: str, value: str, hint: str = "", tone: str = "neutral") -> str:
    tone_class = {
        "up": "of-kpi-up",
        "down": "of-kpi-down",
        "neutral": "",
    }.get(tone, "")
    hint_html = f'<div class="of-kpi-hint {tone_class}">{hint}</div>' if hint else ""
    return f"""
    <div class="of-card of-kpi">
      <div class="of-kpi-label">{label}</div>
      <div class="of-kpi-value">{value}</div>
      {hint_html}
    </div>
    """


def render_dashboard() -> None:
    user_id = st.session_state.user["id"]
    transactions = get_transactions(user_id) or []
    insights = get_insights() or {}
    budgets = get_budgets() or []

    now = datetime.now()

    total_balance = sum(
        t["valor"] if t["tipo"] == "receita" else -t["valor"] for t in transactions
    )
    monthly_expenses = sum(
        t["valor"]
        for t in transactions
        if t["tipo"] == "despesa"
        and datetime.fromisoformat(str(t["data"])[:10]).month == now.month
        and datetime.fromisoformat(str(t["data"])[:10]).year == now.year
    )
    monthly_income = sum(
        t["valor"]
        for t in transactions
        if t["tipo"] == "receita"
        and datetime.fromisoformat(str(t["data"])[:10]).month == now.month
        and datetime.fromisoformat(str(t["data"])[:10]).year == now.year
    )
    monthly_balance = monthly_income - monthly_expenses

    st.markdown(
        """
        <div class="of-page-head">
          <div>
            <p class="of-page-kicker">Visão geral</p>
            <h1 class="of-page-title">Dashboard</h1>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            _kpi("Saldo total", _money(total_balance), "Patrimônio líquido", "up" if total_balance >= 0 else "down"),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            _kpi("Receitas do mês", _money(monthly_income), f"{now.strftime('%b/%Y')}", "up"),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            _kpi("Despesas do mês", _money(monthly_expenses), f"{now.strftime('%b/%Y')}", "down"),
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            _kpi(
                "Resultado do mês",
                _money(monthly_balance),
                "Receitas − despesas",
                "up" if monthly_balance >= 0 else "down",
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.7, 1], gap="medium")

    with left:
        st.markdown(
            '<div class="of-card-title">Receitas vs despesas</div>',
            unsafe_allow_html=True,
        )
        if transactions:
            df = pd.DataFrame(transactions)
            df["data"] = pd.to_datetime(df["data"])
            df["mês"] = df["data"].dt.to_period("M").astype(str)
            pivot = (
                df.groupby(["mês", "tipo"])["valor"]
                .sum()
                .unstack(fill_value=0)
                .reset_index()
                .sort_values("mês")
            )
            if "receita" not in pivot.columns:
                pivot["receita"] = 0
            if "despesa" not in pivot.columns:
                pivot["despesa"] = 0

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=pivot["mês"],
                    y=pivot["receita"],
                    name="Receitas",
                    mode="lines+markers",
                    line=dict(color="#3B82F6", width=3),
                    marker=dict(size=7),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=pivot["mês"],
                    y=pivot["despesa"],
                    name="Despesas",
                    mode="lines+markers",
                    line=dict(color="#F97316", width=3),
                    marker=dict(size=7),
                )
            )
            fig.update_layout(
                margin=dict(l=8, r=8, t=12, b=8),
                height=320,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Manrope, sans-serif", color="#191919", size=12),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(25,25,25,0.06)", zeroline=False),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(
                '<div class="of-empty">Nenhuma transação ainda. Adicione a primeira em Transações.</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            '<div class="of-card-title">Insight</div>',
            unsafe_allow_html=True,
        )
        texto = insights.get("texto") if isinstance(insights, dict) else None
        st.markdown(
            f'<div class="of-card of-insight">{texto or "Registre suas transações para gerar insights."}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="of-card-title" style="margin-top:1rem">Orçamentos</div>',
            unsafe_allow_html=True,
        )
        if budgets:
            rows = []
            for b in budgets[:5]:
                cat = b.get("categoria", "—")
                lim = float(b.get("limite") or 0)
                gasto = float(b.get("gastoAtual") or 0)
                pct = float(b.get("percentual") or (gasto / lim * 100 if lim else 0))
                rows.append(
                    f"""
                    <div class="of-budget-row">
                      <div class="of-budget-top">
                        <span>{cat}</span>
                        <span>{_money(gasto)} / {_money(lim)}</span>
                      </div>
                      <div class="of-budget-bar"><span style="width:{min(pct,100):.0f}%"></span></div>
                    </div>
                    """
                )
            st.markdown(
                f'<div class="of-card">{"".join(rows)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="of-empty">Sem orçamentos carregados.</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="of-card-title">Últimas transações</div>',
        unsafe_allow_html=True,
    )

    if transactions:
        recent = sorted(
            transactions,
            key=lambda t: str(t.get("data", "")),
            reverse=True,
        )[:6]
        rows = []
        for t in recent:
            tipo = t.get("tipo", "")
            badge = "of-badge-in" if tipo == "receita" else "of-badge-out"
            sign = "+" if tipo == "receita" else "−"
            rows.append(
                f"""
                <div class="of-tx-row">
                  <div>
                    <div class="of-tx-cat">{t.get('categoria') or '—'}</div>
                    <div class="of-tx-meta">{t.get('data')} · {t.get('descricao') or tipo}</div>
                  </div>
                  <div class="of-tx-val {badge}">{sign} {_money(float(t.get('valor') or 0))}</div>
                </div>
                """
            )
        st.markdown(
            f'<div class="of-card of-tx-list">{"".join(rows)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="of-empty">Sem lançamentos recentes.</div>',
            unsafe_allow_html=True,
        )
