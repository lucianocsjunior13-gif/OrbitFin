"""Página Transações — CRUDD no shell OrbitFin."""
from __future__ import annotations

from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from components.modals import confirm_action
from services.storage import (
    add_transaction,
    delete_transaction,
    get_transactions,
    update_transaction,
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


def _parse_date(raw):
    if isinstance(raw, datetime):
        return raw.date()
    s = str(raw)[:10]
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        return datetime.now().date()


def _add_dialog(user_id: int) -> None:
    def _form() -> None:
        with st.form("nova_transacao", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                tipo = st.selectbox("Tipo", ["receita", "despesa"])
                valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
                data = st.date_input("Data", value=datetime.now())
            with c2:
                categoria = st.text_input("Categoria", placeholder="Ex: Alimentação, Salário")
                descricao = st.text_input("Descrição", placeholder="Opcional")
                status = st.selectbox("Status", ["pago", "pendente"])

            s1, s2 = st.columns(2)
            with s1:
                submitted = st.form_submit_button("Adicionar", use_container_width=True, type="primary")
            with s2:
                cancel = st.form_submit_button("Cancelar", use_container_width=True)

            if cancel:
                st.rerun()
            if submitted:
                if not categoria.strip():
                    st.error("Informe a categoria.")
                elif valor <= 0:
                    st.error("Valor deve ser maior que zero.")
                else:
                    try:
                        add_transaction(
                            user_id,
                            {
                                "tipo": tipo,
                                "valor": float(valor),
                                "data": data.strftime("%Y-%m-%d"),
                                "categoria": categoria.strip(),
                                "descricao": descricao.strip(),
                                "status": status,
                            },
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao adicionar: {e}")

    if hasattr(st, "dialog"):

        @st.dialog("Nova transação")
        def _dlg() -> None:
            _form()

        _dlg()
    else:
        with st.container(border=True):
            st.markdown("**Nova transação**")
            _form()


def _edit_dialog(user_id: int, selected: dict) -> None:
    tid = selected["id"]
    title = f"Editar · {selected.get('categoria') or 'lançamento'}"

    def _form() -> None:
        with st.form("edit_form_tx"):
            e1, e2 = st.columns(2)
            with e1:
                edit_tipo = st.selectbox(
                    "Tipo",
                    ["receita", "despesa"],
                    index=0 if selected.get("tipo") == "receita" else 1,
                )
                edit_valor = st.number_input(
                    "Valor (R$)",
                    min_value=0.01,
                    step=0.01,
                    value=float(selected.get("valor") or 0.01),
                    format="%.2f",
                )
                edit_data = st.date_input("Data", value=_parse_date(selected.get("data")))
            with e2:
                edit_categoria = st.text_input(
                    "Categoria", value=selected.get("categoria", "") or ""
                )
                edit_descricao = st.text_input(
                    "Descrição", value=selected.get("descricao", "") or ""
                )
                edit_status = st.selectbox(
                    "Status",
                    ["pago", "pendente"],
                    index=0 if selected.get("status") == "pago" else 1,
                )

            s1, s2 = st.columns(2)
            with s1:
                save = st.form_submit_button("Salvar", use_container_width=True, type="primary")
            with s2:
                cancel = st.form_submit_button("Cancelar", use_container_width=True)

            if cancel:
                st.rerun()
            if save:
                ok = update_transaction(
                    user_id,
                    tid,
                    {
                        "tipo": edit_tipo,
                        "valor": float(edit_valor),
                        "data": edit_data.strftime("%Y-%m-%d"),
                        "categoria": edit_categoria.strip(),
                        "descricao": edit_descricao.strip(),
                        "status": edit_status,
                    },
                )
                if ok:
                    st.rerun()
                else:
                    st.error("Erro ao atualizar.")

    if hasattr(st, "dialog"):

        @st.dialog(title)
        def _dlg() -> None:
            _form()

        _dlg()
    else:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            _form()


def _render_list(items: list[dict]) -> None:
    parts = ['<div class="of-card of-tx-list">']
    for t in items:
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
    n = len(items)
    components.html(style + "".join(parts), height=min(70 + 56 * n, 520), scrolling=n > 8)


def render_transactions() -> None:
    user_id = st.session_state.user["id"]
    transactions = get_transactions(user_id) or []

    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown('<div class="of-card-title" style="margin:0">Lançamentos</div>', unsafe_allow_html=True)
    with top_r:
        if st.button("Adicionar transação", key="tx_btn_add", use_container_width=True, type="primary"):
            _add_dialog(user_id)

    if not transactions:
        _html(
            '<div class="of-empty">Nenhuma transação ainda. Clique em '
            "<strong>Adicionar transação</strong> para começar.</div>"
        )
        return

    f1, f2, f3 = st.columns(3)
    with f1:
        tipo_filter = st.selectbox("Tipo", ["Todos", "receita", "despesa"], key="tx_f_tipo")
    with f2:
        status_filter = st.selectbox("Status", ["Todos", "pago", "pendente"], key="tx_f_status")
    with f3:
        cats = ["Todas"] + sorted({t.get("categoria", "") for t in transactions if t.get("categoria")})
        categoria_filter = st.selectbox("Categoria", cats, key="tx_f_cat")

    filtered = list(transactions)
    if tipo_filter != "Todos":
        filtered = [t for t in filtered if t.get("tipo") == tipo_filter]
    if status_filter != "Todos":
        filtered = [t for t in filtered if t.get("status") == status_filter]
    if categoria_filter != "Todas":
        filtered = [t for t in filtered if t.get("categoria") == categoria_filter]

    rec = sum(float(t.get("valor") or 0) for t in filtered if t.get("tipo") == "receita")
    desp = sum(float(t.get("valor") or 0) for t in filtered if t.get("tipo") == "despesa")

    k1, k2, k3 = st.columns(3)
    with k1:
        _html(_kpi("Receitas", _money(rec), f"{len(filtered)} no filtro", "up"))
    with k2:
        _html(_kpi("Despesas", _money(desp), f"{len(filtered)} no filtro", "down"))
    with k3:
        saldo = rec - desp
        _html(
            _kpi(
                "Saldo filtrado",
                _money(saldo),
                "Receitas − despesas",
                "up" if saldo >= 0 else "down",
            )
        )

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)

    if not filtered:
        _html('<div class="of-empty">Nenhuma transação com esses filtros.</div>')
        return

    filtered = sorted(filtered, key=lambda t: str(t.get("data", "")), reverse=True)
    _render_list(filtered)

    st.markdown('<div class="of-gap"></div>', unsafe_allow_html=True)
    st.markdown('<div class="of-card-title">Gerenciar</div>', unsafe_allow_html=True)

    labels = {
        t["id"]: f"{t.get('data','—')} · {t.get('categoria','—')} · {_money(float(t.get('valor') or 0))}"
        for t in filtered
    }
    selected_id = st.selectbox(
        "Selecione um lançamento",
        options=list(labels.keys()),
        format_func=lambda i: labels[i],
        key="tx_manage_id",
    )
    selected = next(t for t in filtered if t["id"] == selected_id)

    a1, a2 = st.columns(2)
    with a1:
        if st.button("Editar", key="tx_btn_edit", use_container_width=True):
            _edit_dialog(user_id, selected)
    with a2:
        if st.button("Excluir", key="tx_btn_delete", use_container_width=True, type="secondary"):
            label = labels[selected_id]

            def _do_delete() -> None:
                if not delete_transaction(user_id, selected_id):
                    st.session_state["tx_delete_error"] = True

            confirm_action(
                title="Excluir lançamento?",
                body=f"Tem certeza que deseja excluir **{label}**? Essa ação não pode ser desfeita.",
                confirm_label="Excluir",
                cancel_label="Cancelar",
                destructive=True,
                on_confirm=_do_delete,
            )

    if st.session_state.pop("tx_delete_error", None):
        st.error("Erro ao excluir.")
