# Delta Spec: Redesign UI — Dashboard + shell

## Objetivo
Redesenhar o **Dashboard** e a **sidebar** no estilo das referências APPROX (cards light, Manrope, whitespace), usando o design system OrbitFin. Páginas Transações/Orçamento/etc. ficam para deltas seguintes (só herdam o shell).

## Design system
| Token | Hex |
|-------|-----|
| Black | `#010103` |
| Background | `#F3F5F7` |
| White | `#FFFFFF` |
| Graphite | `#191919` |
| Font | Manrope |
| Chart accents | azul `#3B82F6` (receita), laranja `#F97316` (despesa) |

## Escopo
- Shell: sidebar clean (logo, nav, user, sair)
- Dashboard: KPI cards, chart receitas/despesas, insight, preview de transações
- Manter storage/Xano intacto

## Critérios de Aceite
- [x] Sidebar sem botões “emoji pill” antigos (`components/sidebar.py`)
- [x] Dashboard com cards de saldo / receitas / despesas / resultado
- [x] Gráfico linha receitas vs despesas (Plotly)
- [x] Insight + preview orçamentos + últimas transações
- [ ] Validar no Streamlit Cloud (QA)
