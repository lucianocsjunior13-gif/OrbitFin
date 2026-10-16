# Delta Spec: Redesign UI — Relatórios

## Objetivo
Redesenhar **Relatórios** no shell OrbitFin: filtros ano/mês, KPIs, donuts, evolução anual e lista do período — sem SQLite direto.

## Design system
Mesmo de `004`–`008`. Charts: receita `#3B82F6`, despesa `#F97316`, saldo `#010103`.

## Escopo
- [x] View `views/reports.py` chart-first (ref. APPROX)
- [x] KPIs + sparklines (série anual)
- [x] Overview linhas (toggle Mensal diário / Anual) + gauge gasto vs receita
- [x] Donuts por categoria
- [x] Barras comparativo mensal (12 meses sempre, zeros se vazio)
- [x] Lista do período via `get_transactions` (não sqlite)
- Storage/API **inalterados**

## Critérios de Aceite
- [ ] Gráficos sempre renderizam (não some a área quando zerado)
- [ ] Toggle Mensal/Anual no overview
- [ ] Funciona com backend Xano
- [ ] Header shell via `main_app`
