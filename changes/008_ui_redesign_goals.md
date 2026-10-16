# Delta Spec: Redesign UI — Metas

## Objetivo
Redesenhar **Metas** como visão de **economia / contenção** (não clone do Orçamento): progresso do que ainda cabe no teto + taxa de poupança do mês.

## Design system
Mesmo de `004`–`007`.

## Escopo
- [x] View `views/goals.py`
- [x] KPI global: taxa de poupança do mês (receitas − despesas)
- [x] KPIs: economia preservada / no caminho / em risco
- [x] Lista por categoria (foco no restante, não só no gasto)
- [x] Ajustar meta (= limite) via modal → `update_budget`
- Storage/API **inalterados** (ainda usa `budget` como teto)

## Critérios de Aceite
- [ ] Visual distinto do Orçamento (copy + KPIs de economia)
- [ ] Dados reais de gastos + resumo mensal
- [ ] Header shell via `main_app`

## Próximo delta
Relatórios.
