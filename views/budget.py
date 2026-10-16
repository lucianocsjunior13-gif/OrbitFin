"""Página Orçamento — limites por categoria no shell OrbitFin."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from services.storage import get_budgets, get_expenses_by_category, update_budget


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
        pct = (gasto / lim * 100) if lim > 0 else 0.0
        rows.append(
            {
                "id": b["id"],
                "categoria": cat,
                "limite": lim,
                "gasto": gasto,
                "restante": lim - gasto,
                "pct": pct,
                "over": lim > 0 and gasto > lim,
            }
        )
    return sorted(rows, key=lambda r: r["pct"], reverse=True)


def _render_list(rows: list[dict]) -> None:
    parts = ['<div class="of-card">']
    for r in rows:
        tone = "over" if r["over"] else ("warn" if r["pct"] >= 85 else "ok")
        bar_w = min(r["pct"], 100)
        chip = "Estourou" if r["over"] else f"{r['pct']:.0f}%"
        sub = (
            f"Ultrapassou {_money(r['gasto'] - r['limite'])}"
            if r["over"]
            else f"{_money(max(r['restante'], 0))} disponível"
        )
        parts.append(
            f'<div class="of-budget-row">'
            f'<div class="of-budget-top">'
            f"<span><strong>{r['categoria']}</strong>"
            f'<span class="of-chip {tone}">{chip}</span></span>'
            f"<span>{_money(r['gasto'])} / {_money(r['limite'])}</span>"
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


def _edit_limit_dialog(row: dict) -> None:
    title = f"Ajustar limite · {row['categoria']}"

    def _body() -> None:
        novo = st.number_input(
            "Novo limite (R$)",
            min_value=0.0,
            step=50.0,
            value=float(row["limite"]),
            format="%.2f",
            key=f"budget_edit_val_{row['id']}",
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Salvar", type="primary", use_container_width=True, key="budget_save"):
                if update_budget(row["id"], float(novo)):
                    st.rerun()
                else:
                    st.error("Erro ao atualizar limite.")
        with c2:
            if st.button("Cancelar", use_container_width=True, key="budget_cancel"):
                st.rerun()

    if hasattr(st, "dialog"):

        @st.dialog(title)
        def _dlg() -> None:
            st.caption(f"Gasto atual: {_money(row['gasto'])}")
            _body()

        _dlg()
    else:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(f"Gasto atual: {_money(row['gasto'])}")
            _body()


def render_budget() -> None:
    user_id = st.session_state.user["id"]
    budgets = get_budgets() or []
    expenses = get_expenses_by_category(user_id) or {}

    if not budgets:
        _html('<div class="of-empty">Nenhum orçamento carregado. Faça o seed de budgets no Xano.</div>')
        return

    rows = _enrich(budgets, expenses)
    total_lim = sum(r["limite"] for r in rows)
    total_gasto = sum(r["gasto"] for r in rows)
    disponivel = total_lim - total_gasto
    over_n = sum(1 for r in rows if r["over"])

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _html(_kpi("Limite total", _money(total_lim), f"{len(rows)} categorias"))
    with k2:
        _html(
            _kpi(
                "Gasto total",
                _money(total_gasto),
                f"{(total_gasto / total_lim * 100) if total_lim else 0:.0f}% do limite",
                "down" if total_gasto > 0 else "neutral",
            )
        )
    with k3:
        _html(
            _kpi(
                "Disponível",
                _money(disponivel),
                "Soma dos limites − gastos",
                "up" if disponivel >= 0 else "down",
            )
        )
    with k4:
        _html(
            _kpi(
                "Estouradas",
                str(over_n),
                "categorias acima do limite",
                "down" if over_n else "up",
            )
        )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="of-card-title">Por categoria</div>', unsafe_allow_html=True)
    _render_list(rows)

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="of-card-title">Ajustar limite</div>', unsafe_allow_html=True)

    labels = {r["id"]: f"{r['categoria']} · {_money(r['limite'])}" for r in rows}
    selected_id = st.selectbox(
        "Categoria",
        options=list(labels.keys()),
        format_func=lambda i: labels[i],
        key="budget_manage_id",
    )
    selected = next(r for r in rows if r["id"] == selected_id)

    if st.button("Editar limite", key="budget_btn_edit", use_container_width=True, type="primary"):
        _edit_limit_dialog(selected)
