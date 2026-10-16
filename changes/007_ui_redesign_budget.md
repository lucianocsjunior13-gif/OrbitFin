# Delta Spec: Redesign UI — Orçamento

## Objetivo
Redesenhar a página **Orçamento** no shell OrbitFin, mantendo leitura de limites + update via storage/Xano.

## Design system
Mesmo de `004`–`006`: `#010103` / `#F3F5F7` / `#FFFFFF` / `#191919` · Manrope · barras de progresso pretas · alerta laranja/vermelho quando estoura.

## Escopo
- [x] View `views/budget.py`
- [x] KPIs: limite total / gasto / disponível / categorias no vermelho
- [x] Lista visual com barras (`components.html`)
- [x] Ajustar limite via select + modal
- Storage/API **inalterados**

## Critérios de Aceite
- [ ] Visual alinhado a Dashboard / Transações
- [ ] Gasto usa `get_expenses_by_category` (transações reais)
- [ ] `update_budget` continua funcionando
- [ ] Header shell via `main_app`

## Próximo delta
Metas / Relatórios.
