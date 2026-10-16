# Delta Spec: Redesign UI — Auth (Login / Registro)

## Objetivo
Redesenhar o OrbitFin com base no design system (cores + Manrope) e referências de dashboard light/clean. **Esta entrega:** separar e redesenhar Login e Registro. Demais páginas em deltas seguintes.

## Design system (fonte: brand kit)
| Token | Hex | Uso |
|-------|-----|-----|
| `--of-black` | `#010103` | CTA primário, painel brand, títulos fortes |
| `--of-background` | `#F3F5F7` | Fundo da página |
| `--of-white` | `#FFFFFF` | Cards / formulários |
| `--of-graphite` | `#191919` | Texto / bordas suaves |
| Font | **Manrope** (Light/Regular/Medium) | 64 / 32 / 14 como escala de referência |

Referência de layout: dashboard light (sidebar, cards arredondados, whitespace) — aplicada no auth como split brand + form.

## Escopo desta entrega
- [x] Delta OpenSpec
- [x] Tokens CSS + inject no Streamlit (`css/orbitfin_theme.css`, `components/theme.py`)
- [x] Views separadas: `views/login.py`, `views/register.py`
- [x] `app.py` roteia `auth_page` ∈ {login, register}
- Dashboard e resto **inalterados** (próxima página = próximo delta)

## Critérios de Aceite
- [ ] Login e Registro são telas distintas, com link entre elas
- [ ] Visual usa Manrope + paleta acima (sem emoji-hero / tabs antigas)
- [ ] Fluxo Xano/storage continua funcionando (register → login → app)
- [ ] Responsivo ok em desktop; mobile usável (form empilha)

## Próximo delta (quando pedir)
Dashboard no estilo APPROX (sidebar clean, KPI cards, chart) — mesma paleta/Manrope.
