# Delta Spec: Redesign UI — Relatórios

## Objetivo
Redesenhar **Relatórios** no shell OrbitFin: filtros ano/mês, KPIs, donuts, evolução anual e lista do período — sem SQLite direto.

## Design system
Mesmo de `004`–`008`. Charts: receita `#3B82F6`, despesa `#F97316`, saldo `#010103`.

## Escopo
- [x] View `views/reports.py`
- [x] KPIs mensais + anuais (cards HTML)
- [x] Donuts despesas/receitas (Plotly, tema limpo)
- [x] Barras + linha evolução anual
- [x] Lista do período via `get_transactions` (não sqlite)
- Storage/API **inalterados**

## Critérios de Aceite
- [ ] Visual alinhado ao resto do app
- [ ] Funciona com backend Xano (sem path sqlite)
- [ ] Header shell via `main_app`
