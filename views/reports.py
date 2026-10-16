"""Página Relatórios — chart-first (ref. APPROX) no shell OrbitFin."""
from __future__ import annotations

import calendar
from collections import defaultdict
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

_LAYOUT = dict(
    margin=dict(l=8, r=8, t=8, b=8),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Manrope, sans-serif", color="#191919", size=12),
    hovermode="x unified",
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=11)),
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


def _month_num(v) -> int:
    try:
        return int(str(v).lstrip("0") or "0")
    except ValueError:
        return 0


def _full_year_df(yearly: dict) -> pd.DataFrame:
    """12 meses sempre (zeros se vazio) — gráfico nunca some."""
    by = {_month_num(r.get("month")): r for r in (yearly.get("monthly_data") or [])}
    rows = []
    for m in range(1, 13):
        r = by.get(m) or {}
        rec = float(r.get("receitas") or 0)
        desp = float(r.get("despesas") or 0)
        rows.append(
            {
                "month": m,
                "label": _MESES_CURTO[m],
                "receitas": rec,
                "despesas": desp,
                "saldo": float(r.get("balance") if r.get("balance") is not None else rec - desp),
            }
        )
    return pd.DataFrame(rows)


def _daily_df(txs: list[dict], year: int, month: int) -> pd.DataFrame:
    rec: dict[int, float] = defaultdict(float)
    desp: dict[int, float] = defaultdict(float)
    for t in txs:
        raw = str(t.get("data") or "")[:10]
        try:
            dt = datetime.fromisoformat(raw)
        except ValueError:
            continue
        if dt.year != year or dt.month != month:
            continue
        v = float(t.get("valor") or 0)
        if t.get("tipo") == "receita":
            rec[dt.day] += v
        elif t.get("tipo") == "despesa":
            desp[dt.day] += v

    n_days = calendar.monthrange(year, month)[1]
    rows = []
    for d in range(1, n_days + 1):
        r, e = rec[d], desp[d]
        rows.append({"label": str(d), "receitas": r, "despesas": e, "saldo": r - e})
    return pd.DataFrame(rows)


def _overview_lines(df: pd.DataFrame, height: int = 360) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["label"],
            y=df["receitas"],
            name="Receitas",
            mode="lines+markers",
            line=dict(color="#3B82F6", width=3),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.08)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["label"],
            y=df["despesas"],
            name="Despesas",
            mode="lines+markers",
            line=dict(color="#F97316", width=3),
            marker=dict(size=6),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["label"],
            y=df["saldo"],
            name="Saldo",
            mode="lines+markers",
            line=dict(color="#010103", width=2, dash="dot"),
            marker=dict(size=5),
        )
    )
    fig.update_layout(
        **_LAYOUT,
        height=height,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(25,25,25,0.06)", zeroline=False),
    )
    return fig


def _bars_year(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["label"], y=df["receitas"], name="Receitas", marker_color="#3B82F6"))
    fig.add_trace(go.Bar(x=df["label"], y=df["despesas"], name="Despesas", marker_color="#F97316"))
    fig.add_trace(
        go.Scatter(
            x=df["label"],
            y=df["saldo"],
            name="Saldo",
            mode="lines+markers",
            line=dict(color="#010103", width=3),
            marker=dict(size=6),
        )
    )
    fig.update_layout(
        **_LAYOUT,
        height=320,
        barmode="group",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(25,25,25,0.06)", zeroline=False),
    )
    return fig


def _gauge_spend(desp: float, rec: float) -> go.Figure:
    ceiling = max(rec, desp, 1.0)
    pct = min(desp / ceiling * 100, 100) if ceiling else 0
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=desp,
            number={"prefix": "R$ ", "valueformat": ",.0f", "font": {"size": 22, "family": "Manrope"}},
            title={"text": "Despesas no período", "font": {"size": 13, "color": "#191919"}},
            gauge={
                "axis": {"range": [0, ceiling], "tickwidth": 0, "tickcolor": "transparent"},
                "bar": {"color": "#F97316"},
                "bgcolor": "#F3F5F7",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, ceiling * 0.6], "color": "#EEF2FF"},
                    {"range": [ceiling * 0.6, ceiling * 0.9], "color": "#FFEDD5"},
                    {"range": [ceiling * 0.9, ceiling], "color": "#FEE2E2"},
                ],
                "threshold": {
                    "line": {"color": "#010103", "width": 2},
                    "thickness": 0.75,
                    "value": rec if rec > 0 else ceiling,
                },
            },
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=10),
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, sans-serif", color="#191919"),
        annotations=[
            dict(
                text=f"{pct:.0f}% das receitas" if rec > 0 else "sem receitas no período",
                x=0.5,
                y=0.05,
                showarrow=False,
                font=dict(size=11, color="rgba(25,25,25,0.5)"),
            )
        ],
    )
    return fig


def _donut(df: pd.DataFrame) -> go.Figure:
    colors = ["#010103", "#3B82F6", "#F97316", "#64748B", "#94A3B8", "#CBD5E1", "#191919"]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["categoria"],
                values=df["total"],
                hole=0.62,
                textinfo="percent",
                marker=dict(colors=colors[: len(df)], line=dict(color="#F3F5F7", width=2)),
            )
        ]
    )
    fig.update_layout(
        **_LAYOUT,
        height=300,
        margin=dict(l=8, r=8, t=8, b=8),
        legend=dict(orientation="h", y=-0.08, font=dict(size=11)),
    )
    return fig


def _sparkline(series: list[float], color: str) -> go.Figure:
    fills = {
        "#F97316": "rgba(249,115,22,0.12)",
        "#010103": "rgba(1,1,3,0.08)",
        "#3B82F6": "rgba(59,130,246,0.12)",
    }
    fill = fills.get(color, "rgba(59,130,246,0.12)")
    fig = go.Figure(
        go.Scatter(
            y=series,
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=fill,
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=56,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
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
    all_txs = get_transactions(user_id) or []

    f1, f2, f3 = st.columns([1, 1, 1.2])
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
    with f3:
        mode = st.radio(
            "Visão do gráfico",
            ["Mensal", "Anual"],
            horizontal=True,
            key="rep_chart_mode",
        )

    monthly = get_monthly_summary(user_id, year, month) or {}
    yearly = get_yearly_summary(user_id, year) or {}
    year_df = _full_year_df(yearly)
    period_txs = _period_txs(user_id, year, month)

    rec_m = float(monthly.get("total_receitas") or 0)
    desp_m = float(monthly.get("total_despesas") or 0)
    bal_m = float(monthly.get("balance") if monthly.get("balance") is not None else rec_m - desp_m)
    savings = (bal_m / rec_m * 100) if rec_m > 0 else 0.0

    # ——— KPIs + sparklines ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _html(_kpi("Receitas", _money(rec_m), f"{_MESES[month][:3]} · mês", "up"))
        st.plotly_chart(
            _sparkline(year_df["receitas"].tolist(), "#3B82F6"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with k2:
        _html(_kpi("Despesas", _money(desp_m), f"{_MESES[month][:3]} · mês", "down"))
        st.plotly_chart(
            _sparkline(year_df["despesas"].tolist(), "#F97316"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with k3:
        _html(_kpi("Saldo", _money(bal_m), "receitas − despesas", "up" if bal_m >= 0 else "down"))
        st.plotly_chart(
            _sparkline(year_df["saldo"].tolist(), "#010103"),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with k4:
        _html(
            _kpi(
                "Poupança",
                f"{savings:.0f}%",
                "sobre receitas do mês",
                "up" if savings >= 0 else "down",
            )
        )
        # sparkline: taxa mensal aproximada
        rates = []
        for _, row in year_df.iterrows():
            rates.append((row["saldo"] / row["receitas"] * 100) if row["receitas"] else 0)
        st.plotly_chart(
            _sparkline(rates, "#3B82F6"),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # ——— Overview (hero chart) + gauge ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.7, 1], gap="medium")

    with left:
        if mode == "Anual":
            total = float(year_df["receitas"].sum())
            st.markdown(
                f'<div class="of-card-title">Visão geral · {year}'
                f' <span style="color:#16A34A;font-size:12px;font-weight:600;margin-left:.5rem">'
                f"{_money(total)} receitas</span></div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                _overview_lines(year_df),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            daily = _daily_df(all_txs, year, month)
            st.markdown(
                f'<div class="of-card-title">Visão geral · {_MESES[month]} {year}'
                f' <span style="color:#16A34A;font-size:12px;font-weight:600;margin-left:.5rem">'
                f"{_money(rec_m)}</span></div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                _overview_lines(daily, height=360),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            if not period_txs:
                st.caption("Sem lançamentos neste mês — o gráfico mostra a grade diária zerada.")

    with right:
        st.markdown('<div class="of-card-title">Gasto vs receita</div>', unsafe_allow_html=True)
        if mode == "Anual":
            st.plotly_chart(
                _gauge_spend(
                    float(year_df["despesas"].sum()),
                    float(year_df["receitas"].sum()),
                ),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.plotly_chart(
                _gauge_spend(desp_m, rec_m),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    # ——— Donuts categoria ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2, gap="medium")
    with d1:
        st.markdown('<div class="of-card-title">Despesas por categoria</div>', unsafe_allow_html=True)
        exp = monthly.get("expenses_by_category") or []
        if exp:
            st.plotly_chart(_donut(pd.DataFrame(exp)), use_container_width=True, config={"displayModeBar": False})
        else:
            _html('<div class="of-empty">Sem despesas neste mês para montar o donut.</div>')
    with d2:
        st.markdown('<div class="of-card-title">Receitas por categoria</div>', unsafe_allow_html=True)
        inc = monthly.get("income_by_category") or []
        if inc:
            st.plotly_chart(_donut(pd.DataFrame(inc)), use_container_width=True, config={"displayModeBar": False})
        else:
            _html('<div class="of-empty">Sem receitas neste mês para montar o donut.</div>')

    # ——— Barras anuais (sempre) ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="of-card-title">Comparativo mensal · {year}</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(_bars_year(year_df), use_container_width=True, config={"displayModeBar": False})

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

    # ——— Lista ———
    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="of-card-title">Lançamentos · {_MESES[month]} {year}</div>',
        unsafe_allow_html=True,
    )
    if period_txs:
        _render_tx_list(period_txs)
        if len(period_txs) > 40:
            st.caption(f"Mostrando 40 de {len(period_txs)} lançamentos.")
    else:
        _html('<div class="of-empty">Nenhuma transação neste período. Cadastre em Transações.</div>')
