# Delta Spec: Seed de budgets + update de orçamento/insight no Xano

## Objetivo
Completar o que faltou do delta 002: orçamentos padrão no cadastro, `PUT` de budget e update de insight, e marcar E2E Streamlit como aceito (app em https://orbitfin.streamlit.app/).

## Escopo
- Seed de categorias padrão no `register` + lazy-seed no `GET budgets` (contas antigas)
- `PUT /budgets/{budget_id}`
- `PUT /insights` (texto)
- Wire em `xano_storage.py`
- Atualizar critérios do `002` / `ROADMAP`

## Critérios de Aceite
- [x] Endpoints pushed no Xano (`PUT budgets/{id}`, `PUT insights`, seed no `register` + lazy seed no `GET budgets`)
- [ ] Conta nova nasce com budgets padrão + insight inicial (validar no app)
- [ ] Conta antiga sem budget recebe seed no primeiro `GET /budgets` (abrir Orçamento)
- [ ] Atualizar limite na UI persiste no Xano
- [x] Docs 002/ROADMAP com E2E Streamlit marcado

## Nota
API Group local vive em `xano/api/orbit_fin/` (não `orbitfin/` — pull renomeia e duplica GUID).
