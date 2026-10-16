"""Página Relatórios — análises mensal/anual no shell OrbitFin."""
from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from services.storage import get_monthly_summary, get_transactions, get_yearly_summary

_MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
_MESES_CURTO = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}

_CHART_LAYOUT = dict(
    margin=dict(l=8, r=8, t=12, b=8),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Manrope, sans-serif", color="#191919", size=12),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    hovermode="x unified",
)


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


def _html(html: str) -> None:
    flat = " ".join(line.strip() for line in html.splitlines() if line.strip())
    st.markdown(flat, unsafe_allow_html=True)


def _donut(df: pd.DataFrame, title: str) -> go.Figure:
    colors = ["#010103", "#3B82F6", "#F97316", "#64748B", "#94A3B8", "#CBD5E1", "#191919"]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["categoria"],
                values=df["total"],
                hole=0.58,
                textinfo="percent",
                marker=dict(colors=colors[: len(df)], line=dict(color="#F3F5F7", width=2)),
            )
        ]
    )
    fig.update_layout(
        **_CHART_LAYOUT,
        height=280,
        title=dict(text=title, font=dict(size=13, color="#010103"), x=0, xanchor="left"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.05, font=dict(size=11)),
        margin=dict(l=8, r=8, t=40, b=8),
    )
    return fig


def _period_txs(user_id: int, year: int, month: int) -> list[dict]:
    out = []
    for t in get_transactions(user_id) or []:
        raw = str(t.get("data") or "")[:10]
        try:
            dt = datetime.fromisoformat(raw)
        except ValueError:
            continue
        if dt.year == year and dt.month == month:
            out.append(t)
    return sorted(out, key=lambda x: str(x.get("data", "")), reverse=True)


def _render_tx_list(items: list[dict]) -> None:
    parts = ['<div class="of-card of-tx-list">']
    for t in items[:40]:
        tipo = t.get("tipo", "")
        badge = "of-badge-in" if tipo == "receita" else "of-badge-out"
        sign = "+" if tipo == "receita" else "−"
        cat = t.get("categoria") or "—"
        desc = t.get("descricao") or tipo
        data = t.get("data") or "—"
        status = t.get("status") or "—"
        val = _money(float(t.get("valor") or 0))
        parts.append(
            f'<div class="of-tx-row"><div>'
            f'<div class="of-tx-cat">{cat}'
            f'<span class="of-chip">{status}</span></div>'
            f'<div class="of-tx-meta">{data} · {desc}</div></div>'
            f'<div class="of-tx-val {badge}">{sign} {val}</div></div>'
        )
    parts.append("</div>")
    style = """
    <style>
      body{margin:0;font-family:Manrope,system-ui,sans-serif;background:transparent}
      .of-card{background:#fff;border:1px solid rgba(25,25,25,.07);border-radius:16px;
        padding:.35rem 1.15rem;box-shadow:0 8px 24px rgba(1,1,3,.03)}
      .of-tx-row{display:flex;justify-content:space-between;align-items:center;gap:1rem;
        padding:.85rem 0;border-bottom:1px solid rgba(25,25,25,.06)}
      .of-tx-row:last-child{border-bottom:none}
      .of-tx-cat{font-size:14px;font-weight:700;color:#010103}
      .of-tx-meta{font-size:12px;color:rgba(25,25,25,.45);margin-top:.15rem}
      .of-tx-val{font-size:14px;font-weight:700;white-space:nowrap}
      .of-badge-in{color:#16A34A}.of-badge-out{color:#EA580C}
      .of-chip{display:inline-block;margin-left:.45rem;padding:.12rem .5rem;border-radius:999px;
        font-size:10px;font-weight:600;background:#F3F5F7;color:#191919;text-transform:uppercase;
        letter-spacing:.04em;vertical-align:middle}
    </style>
    """
    n = min(len(items), 40)
    components.html(style + "".join(parts), height=min(70 + 56 * n, 480), scrolling=n > 7)


def render_reports() -> None:
    user_id = st.session_state.user["id"]
    now = datetime.now()
    years = list(range(now.year - 5, now.year + 1))

    f1, f2 = st.columns(2)
    with f1:
        year = st.selectbox("Ano", options=years, index=len(years) - 1, key="rep_year")
    with f2:
        month = st.selectbox(
            "Mês",
            options=list(range(1, 13)),
            format_func=lambda m: _MESES[m],
            index=now.month - 1,
            key="rep_month",
        )

    monthly = get_monthly_summary(user_id, year, month) or {}
    yearly = get_yearly_summary(user_id, year) or {}

    rec_m = float(monthly.get("total_receitas") or 0)
    desp_m = float(monthly.get("total_despesas") or 0)
    bal_m = float(monthly.get("balance") if monthly.get("balance") is not None else rec_m - desp_m)
    savings = (bal_m / rec_m * 100) if rec_m > 0 else 0.0

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="of-card-title">{_MESES[month]} {year}</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _html(_kpi("Receitas", _money(rec_m), "no mês", "up"))
    with k2:
        _html(_kpi("Despesas", _money(desp_m), "no mês", "down"))
    with k3:
        _html(_kpi("Saldo", _money(bal_m), "receitas − despesas", "up" if bal_m >= 0 else "down"))
    with k4:
        _html(
            _kpi(
                "Poupança",
                f"{savings:.0f}%",
                "sobre receitas do mês",
                "up" if savings >= 0 else "down",
            )
        )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown('<div class="of-card-title">Despesas por categoria</div>', unsafe_allow_html=True)
        exp = monthly.get("expenses_by_category") or []
        if exp:
            fig = _donut(pd.DataFrame(exp), "")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            _html('<div class="of-empty">Sem despesas neste mês.</div>')

    with c2:
        st.markdown('<div class="of-card-title">Receitas por categoria</div>', unsafe_allow_html=True)
        inc = monthly.get("income_by_category") or []
        if inc:
            fig = _donut(pd.DataFrame(inc), "")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            _html('<div class="of-empty">Sem receitas neste mês.</div>')

    # ——— Ano ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="of-card-title">Ano {year}</div>', unsafe_allow_html=True)

    rec_y = float(yearly.get("total_receitas") or 0)
    desp_y = float(yearly.get("total_despesas") or 0)
    bal_y = float(yearly.get("balance") if yearly.get("balance") is not None else rec_y - desp_y)

    y1, y2, y3 = st.columns(3)
    with y1:
        _html(_kpi("Receitas anuais", _money(rec_y), str(year), "up"))
    with y2:
        _html(_kpi("Despesas anuais", _money(desp_y), str(year), "down"))
    with y3:
        _html(_kpi("Saldo anual", _money(bal_y), str(year), "up" if bal_y >= 0 else "down"))

    monthly_rows = yearly.get("monthly_data") or []
    if monthly_rows:
        df = pd.DataFrame(monthly_rows)

        def _month_num(v) -> int:
            try:
                return int(str(v).lstrip("0") or "0")
            except ValueError:
                return 0

        df["month_n"] = df["month"].map(_month_num)
        df["label"] = df["month_n"].map(_MESES_CURTO)

        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=df["label"], y=df["receitas"], name="Receitas", marker_color="#3B82F6")
        )
        fig.add_trace(
            go.Bar(x=df["label"], y=df["despesas"], name="Despesas", marker_color="#F97316")
        )
        fig.add_trace(
            go.Scatter(
                x=df["label"],
                y=df["balance"],
                name="Saldo",
                mode="lines+markers",
                line=dict(color="#010103", width=3),
                marker=dict(size=6),
            )
        )
        fig.update_layout(
            **_CHART_LAYOUT,
            height=340,
            barmode="group",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(25,25,25,0.06)", zeroline=False),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        _html('<div class="of-empty">Sem dados anuais para este período.</div>')

    # ——— Lista período ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="of-card-title">Lançamentos · {_MESES[month]} {year}</div>',
        unsafe_allow_html=True,
    )

    txs = _period_txs(user_id, year, month)
    if txs:
        _render_tx_list(txs)
        if len(txs) > 40:
            st.caption(f"Mostrando 40 de {len(txs)} lançamentos.")
    else:
        _html('<div class="of-empty">Nenhuma transação neste período.</div>')
