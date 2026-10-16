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
- [x] Sidebar texto + ícones Lucide (SVG via iframe), sem bg/borda nos links
- [x] Collapse da sidebar só no mobile; desktop sempre expanded
- [x] Header shell (busca + actions + título) em todas as páginas logadas
- [x] Dashboard com cards de saldo / receitas / despesas / resultado
- [x] Gráfico linha receitas vs despesas (Plotly)
- [x] Insight + orçamentos (components.html) + últimas transações — sem HTML cru
- [ ] Validar no Streamlit Cloud (QA)
