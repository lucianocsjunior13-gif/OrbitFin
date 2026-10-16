"""Página Metas — economia / contenção por categoria (shell OrbitFin)."""
from __future__ import annotations

from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from services.storage import (
    get_budgets,
    get_expenses_by_category,
    get_monthly_summary,
    update_budget,
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


def _enrich(budgets: list[dict], expenses: dict[str, float]) -> list[dict]:
    rows = []
    for b in budgets:
        cat = b.get("categoria") or "—"
        lim = float(b.get("limite") or 0)
        gasto = float(expenses.get(cat, 0))
        restante = lim - gasto
        # % da meta de contenção ainda intacta
        room_pct = (restante / lim * 100) if lim > 0 else 0.0
        if lim <= 0:
            status = "none"
        elif restante <= 0:
            status = "done"  # teto consumido / estourou
        elif restante <= lim * 0.1:
            status = "risk"
        else:
            status = "ok"
        rows.append(
            {
                "id": b["id"],
                "categoria": cat,
                "limite": lim,
                "gasto": gasto,
                "restante": restante,
                "room_pct": max(room_pct, 0.0),
                "status": status,
            }
        )
    order = {"risk": 0, "done": 1, "ok": 2, "none": 3}
    return sorted(rows, key=lambda r: (order.get(r["status"], 9), r["room_pct"]))


def _render_list(rows: list[dict]) -> None:
    parts = ['<div class="of-card">']
    chip_map = {
        "ok": ("No caminho", "ok"),
        "risk": ("Em risco", "warn"),
        "done": ("Teto atingido", "over"),
        "none": ("Sem meta", "ok"),
    }
    for r in rows:
        label, tone = chip_map[r["status"]]
        # barra = quanto do teto ainda sobra (economia preservada)
        bar_w = min(r["room_pct"], 100) if r["limite"] > 0 else 0
        if r["status"] == "done":
            sub = (
                f"Gastou {_money(r['gasto'])} de {_money(r['limite'])}"
                + (
                    f" · ultrapassou {_money(r['gasto'] - r['limite'])}"
                    if r["gasto"] > r["limite"]
                    else ""
                )
            )
        elif r["status"] == "none":
            sub = "Defina um limite para acompanhar esta meta"
        else:
            sub = f"{_money(max(r['restante'], 0))} ainda cabem no teto"
        parts.append(
            f'<div class="of-budget-row">'
            f'<div class="of-budget-top">'
            f"<span><strong>{r['categoria']}</strong>"
            f'<span class="of-chip {tone}">{label}</span></span>'
            f"<span>{_money(max(r['restante'], 0))} / {_money(r['limite'])}</span>"
            f"</div>"
            f'<div class="of-budget-bar {tone}"><span style="width:{bar_w:.0f}%"></span></div>'
            f'<div class="of-budget-sub">{sub}</div></div>'
        )
    parts.append("</div>")
    style = """
    <style>
      body{margin:0;font-family:Manrope,system-ui,sans-serif;background:transparent}
      .of-card{background:#fff;border:1px solid rgba(25,25,25,.07);border-radius:16px;
        padding:1.1rem 1.15rem;box-shadow:0 8px 24px rgba(1,1,3,.03)}
      .of-budget-row{margin-bottom:1.05rem}
      .of-budget-row:last-child{margin-bottom:0}
      .of-budget-top{display:flex;justify-content:space-between;align-items:baseline;
        font-size:13px;color:#191919;margin-bottom:.4rem;gap:.75rem}
      .of-budget-top strong{font-size:14px;color:#010103;margin-right:.35rem}
      .of-budget-bar{height:7px;background:#F3F5F7;border-radius:999px;overflow:hidden}
      .of-budget-bar>span{display:block;height:100%;background:#010103;border-radius:999px}
      .of-budget-bar.warn>span{background:#EA580C}
      .of-budget-bar.over>span{background:#DC2626}
      .of-budget-sub{margin-top:.3rem;font-size:11px;color:rgba(25,25,25,.45)}
      .of-chip{display:inline-block;margin-left:.35rem;padding:.1rem .45rem;border-radius:999px;
        font-size:10px;font-weight:600;background:#F3F5F7;color:#191919;text-transform:uppercase;
        letter-spacing:.04em;vertical-align:middle}
      .of-chip.warn{background:#FFF7ED;color:#C2410C}
      .of-chip.over{background:#FEF2F2;color:#B91C1C}
    </style>
    """
    n = len(rows)
    components.html(style + "".join(parts), height=min(90 + 78 * n, 560), scrolling=n > 6)


def _edit_goal_dialog(row: dict) -> None:
    title = f"Ajustar meta · {row['categoria']}"

    def _body() -> None:
        novo = st.number_input(
            "Teto da meta (R$)",
            min_value=0.0,
            step=50.0,
            value=float(row["limite"]),
            format="%.2f",
            key=f"goal_edit_val_{row['id']}",
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Salvar", type="primary", use_container_width=True, key="goal_save"):
                if update_budget(row["id"], float(novo)):
                    st.rerun()
                else:
                    st.error("Erro ao atualizar meta.")
        with c2:
            if st.button("Cancelar", use_container_width=True, key="goal_cancel"):
                st.rerun()

    if hasattr(st, "dialog"):

        @st.dialog(title)
        def _dlg() -> None:
            st.caption(
                f"Gasto atual {_money(row['gasto'])} · "
                f"restante {_money(max(row['restante'], 0))}"
            )
            _body()

        _dlg()
    else:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            _body()


def render_goals() -> None:
    user_id = st.session_state.user["id"]
    now = datetime.now()
    budgets = get_budgets() or []
    expenses = get_expenses_by_category(user_id) or {}
    monthly = get_monthly_summary(user_id, now.year, now.month) or {}

    rec = float(monthly.get("total_receitas") or 0)
    desp = float(monthly.get("total_despesas") or 0)
    balance = float(monthly.get("balance") if monthly.get("balance") is not None else rec - desp)
    savings_rate = (balance / rec * 100) if rec > 0 else 0.0

    if not budgets:
        _html('<div class="of-empty">Nenhuma meta disponível. Cadastre limites em Orçamento.</div>')
        return

    rows = _enrich(budgets, expenses)
    preservada = sum(max(r["restante"], 0) for r in rows if r["limite"] > 0)
    ok_n = sum(1 for r in rows if r["status"] == "ok")
    risk_n = sum(1 for r in rows if r["status"] in ("risk", "done"))

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _html(
            _kpi(
                "Poupança do mês",
                f"{savings_rate:.0f}%",
                f"{_money(balance)} de saldo · {now.strftime('%b/%Y')}",
                "up" if savings_rate >= 0 else "down",
            )
        )
    with k2:
        _html(_kpi("Economia preservada", _money(preservada), "Soma do que ainda cabe nos tetos", "up"))
    with k3:
        _html(_kpi("No caminho", str(ok_n), "metas com folga > 10%", "up"))
    with k4:
        _html(
            _kpi(
                "Atenção",
                str(risk_n),
                "em risco ou teto atingido",
                "down" if risk_n else "up",
            )
        )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    _html(
        '<div class="of-empty" style="border-style:solid;padding:.85rem 1.1rem">'
        "Cada meta = teto de gasto por categoria. A barra mostra quanto ainda sobra para gastar "
        "sem estourar — quanto maior, melhor a contenção."
        "</div>"
    )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="of-card-title">Metas por categoria</div>', unsafe_allow_html=True)
    _render_list(rows)

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="of-card-title">Ajustar meta</div>', unsafe_allow_html=True)

    labels = {r["id"]: f"{r['categoria']} · teto {_money(r['limite'])}" for r in rows}
    selected_id = st.selectbox(
        "Categoria",
        options=list(labels.keys()),
        format_func=lambda i: labels[i],
        key="goal_manage_id",
    )
    selected = next(r for r in rows if r["id"] == selected_id)

    if st.button("Editar meta", key="goal_btn_edit", use_container_width=True, type="primary"):
        _edit_goal_dialog(selected)
