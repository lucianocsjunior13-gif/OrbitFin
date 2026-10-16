# ROADMAP.md: OrbitFin

## Integração Xano (delta `changes/002_...`)

- [x] **Fase 0–2:** OpenSpec + CLI + scaffold `xano/`
- [x] **Fase 3:** Tabelas `user`, `transacao`, `budget`, `insight` (XanoScript)
- [x] **Fase 4–5:** API Group `orbitfin` + endpoints; push/pull OK
- [x] **Fase 6:** `.gitignore` + `st.secrets` (exemplo versionado)
- [x] **Fase 7:** Adapter `services/storage.py` (SQLite ↔ Xano)
- [ ] **Fase 8:** Teste ponta a ponta Streamlit ↔ Xano (pendente — outro ambiente/pessoa)
- [ ] Endpoints faltando no Xano: `PUT budgets`, update insight
- [ ] Seed de budgets padrão por usuário no register

## Roadmap produto original

- [x] **Fase 1: Configuração Inicial**
  - [x] Estruturação do projeto com OpenSpec
  - [x] Configuração do banco de dados e endpoints base (Auth e Transações) no Xano
  - [ ] Criação do ambiente virtual Python e instalação do Streamlit e `requests` (na máquina do desenvolvedor / QA)

- [x] **Fase 2: Autenticação e Telas Base** (código pronto; validação E2E Streamlit pendente)
  - [x] Tela de Login/Cadastro no Streamlit preparada para Xano (`storage` + `enabled=true`)
  - [x] Páginas principais (Dashboard, Transações, etc.) em `app.py`

- [x] **Fase 3: Funcionalidades Core** (código pronto; E2E pendente)
  - [x] CRUD de transações via interface (via adapter Xano)
  - [x] Gráficos de resumo financeiro no dashboard

- [ ] **Fase 4: Refinamento e Testes**
  - [ ] Validações de campos, tratamento de erros de API e polimento visual
  - [ ] QA Streamlit com `secrets.toml` apontando para `api:orbitfin`
