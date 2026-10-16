"""Dashboard redesenhado — KPIs + chart + insight (ref. APPROX)."""
from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from components.header import render_header
from services.storage import get_budgets, get_insights, get_transactions


def _money(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _kpi(label: str, value: str, hint: str = "", tone: str = "neutral") -> str:
    tone_class = {"up": "of-kpi-up", "down": "of-kpi-down", "neutral": ""}.get(tone, "")
    hint_html = f'<div class="of-kpi-hint {tone_class}">{hint}</div>' if hint else ""
    return (
        f'<div class="of-card of-kpi">'
        f'<div class="of-kpi-label">{label}</div>'
        f'<div class="of-kpi-value">{value}</div>'
        f"{hint_html}</div>"
    )


def _html_block(html: str, height: int | None = None) -> None:
    """Render HTML sem o Markdown transformar indentação em code fence."""
    flat = " ".join(line.strip() for line in html.splitlines() if line.strip())
    if height:
        components.html(
            f"<link href='https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap' rel='stylesheet'>"
            f"<style>body{{margin:0;font-family:Manrope,sans-serif;}}</style>{flat}",
            height=height,
            scrolling=False,
        )
    else:
        st.markdown(flat, unsafe_allow_html=True)


def render_dashboard() -> None:
    render_header("dashboard")

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

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _html_block(
            _kpi("Saldo total", _money(total_balance), "Patrimônio líquido", "up" if total_balance >= 0 else "down")
        )
    with c2:
        _html_block(_kpi("Receitas do mês", _money(monthly_income), now.strftime("%b/%Y"), "up"))
    with c3:
        _html_block(_kpi("Despesas do mês", _money(monthly_expenses), now.strftime("%b/%Y"), "down"))
    with c4:
        _html_block(
            _kpi(
                "Resultado do mês",
                _money(monthly_balance),
                "Receitas − despesas",
                "up" if monthly_balance >= 0 else "down",
            )
        )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.7, 1], gap="medium")

    with left:
        st.markdown('<div class="of-card-title">Receitas vs despesas</div>', unsafe_allow_html=True)
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
            _html_block('<div class="of-empty">Nenhuma transação ainda. Adicione a primeira em Transações.</div>')

    with right:
        st.markdown('<div class="of-card-title">Insight</div>', unsafe_allow_html=True)
        texto = insights.get("texto") if isinstance(insights, dict) else None
        _html_block(
            f'<div class="of-card of-insight">{texto or "Registre suas transações para gerar insights."}</div>'
        )

        st.markdown(
            '<div class="of-card-title" style="margin-top:1rem">Orçamentos</div>',
            unsafe_allow_html=True,
        )
        if budgets:
            parts = ['<div class="of-card">']
            for b in budgets[:6]:
                cat = b.get("categoria", "—")
                lim = float(b.get("limite") or 0)
                gasto = float(b.get("gastoAtual") or 0)
                pct = float(b.get("percentual") or (gasto / lim * 100 if lim else 0))
                parts.append(
                    f'<div class="of-budget-row">'
                    f'<div class="of-budget-top"><span>{cat}</span>'
                    f"<span>{_money(gasto)} / {_money(lim)}</span></div>"
                    f'<div class="of-budget-bar"><span style="width:{min(pct, 100):.0f}%"></span></div>'
                    f"</div>"
                )
            parts.append("</div>")
            # components.html isola do markdown parser (evita HTML virar texto)
            style = """
            <style>
              body{margin:0;font-family:Manrope,system-ui,sans-serif}
              .of-card{background:#fff;border:1px solid rgba(25,25,25,.07);border-radius:16px;padding:1.1rem 1.15rem}
              .of-budget-row{margin-bottom:.85rem}
              .of-budget-row:last-child{margin-bottom:0}
              .of-budget-top{display:flex;justify-content:space-between;font-size:12px;color:#191919;margin-bottom:.35rem;gap:.5rem}
              .of-budget-bar{height:6px;background:#F3F5F7;border-radius:999px;overflow:hidden}
              .of-budget-bar>span{display:block;height:100%;background:#010103;border-radius:999px}
            </style>
            """
            components.html(style + "".join(parts), height=min(80 + 52 * len(budgets[:6]), 360), scrolling=False)
        else:
            _html_block('<div class="of-empty">Sem orçamentos carregados.</div>')

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="of-card-title">Últimas transações</div>', unsafe_allow_html=True)

    if transactions:
        recent = sorted(transactions, key=lambda t: str(t.get("data", "")), reverse=True)[:6]
        parts = ['<div class="of-card of-tx-list">']
        for t in recent:
            tipo = t.get("tipo", "")
            badge = "of-badge-in" if tipo == "receita" else "of-badge-out"
            sign = "+" if tipo == "receita" else "−"
            cat = t.get("categoria") or "—"
            desc = t.get("descricao") or tipo
            data = t.get("data")
            val = _money(float(t.get("valor") or 0))
            parts.append(
                f'<div class="of-tx-row"><div>'
                f'<div class="of-tx-cat">{cat}</div>'
                f'<div class="of-tx-meta">{data} · {desc}</div></div>'
                f'<div class="of-tx-val {badge}">{sign} {val}</div></div>'
            )
        parts.append("</div>")
        style = """
        <style>
          body{margin:0;font-family:Manrope,system-ui,sans-serif}
          .of-card{background:#fff;border:1px solid rgba(25,25,25,.07);border-radius:16px;padding:.35rem 1.15rem;box-shadow:0 8px 24px rgba(1,1,3,.03)}
          .of-tx-row{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:.85rem 0;border-bottom:1px solid rgba(25,25,25,.06)}
          .of-tx-row:last-child{border-bottom:none}
          .of-tx-cat{font-size:14px;font-weight:600;color:#010103}
          .of-tx-meta{font-size:12px;color:rgba(25,25,25,.45);margin-top:.15rem}
          .of-tx-val{font-size:14px;font-weight:700;white-space:nowrap}
          .of-badge-in{color:#16A34A}.of-badge-out{color:#EA580C}
        </style>
        """
        components.html(style + "".join(parts), height=min(70 + 56 * len(recent), 400), scrolling=False)
    else:
        _html_block('<div class="of-empty">Sem lançamentos recentes.</div>')
