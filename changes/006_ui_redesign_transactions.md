# Delta Spec: Redesign UI — Transações

## Objetivo
Redesenhar a página **Transações** no shell OrbitFin (Manrope + paleta + header/sidebar), mantendo CRUD via storage/Xano.

## Design system
Mesmo de `004` / `005`: `#010103` / `#F3F5F7` / `#FFFFFF` / `#191919` · Manrope · badges receita `#16A34A` / despesa `#EA580C`.

## Escopo
- [x] View `views/transactions.py` (sai do monólito `app.py`)
- [x] KPIs do período filtrado (receitas / despesas / qtd)
- [x] Form “Nova transação” limpo (expander)
- [x] Filtros tipo / status / categoria
- [x] Lista em cards (sem emoji-hero / pills coloridos)
- [x] Editar / excluir preservados
- Storage/API **inalterados**

## Critérios de Aceite
- [ ] Visual alinhado ao Dashboard (cards, tipografia, sem emoji decorativo)
- [ ] Adicionar / editar / excluir continua funcionando com Xano
- [ ] Filtros aplicam na lista e nos KPIs
- [ ] Header shell já renderizado por `main_app`
- [x] Modal confirmar exclusão + modal editar (`st.dialog`)
- [x] Nav sidebar via `st.button` (iframe/`?nav=` quebrava)

## Próximo delta
Orçamento / Metas / Relatórios.
