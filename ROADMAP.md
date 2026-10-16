# ROADMAP.md: Plano de Desenvolvimento e Evolução — OrbitFin (Grupo Marte)

O desenvolvimento do **OrbitFin** é estruturado em fases incrementais seguindo a metodologia **OpenSpec** e a proposta de desenvolvimento colaborativo da disciplina.

---

## 1. Documentação OpenSpec e Identidade Grupo Marte
- [x] **Fase 1: Concepção, Identidade Visual e Especificação OpenSpec**
  - [x] Definição da visão do produto, identidade **Orbit / OrbitFin (Grupo Marte)** e paleta oficial de 3 cores (`#E05638`, `#1A2238`, `#F4F6F8`) em [`PRODUCT.md`](./PRODUCT.md).
  - [x] Mapeamento da arquitetura **Python + Streamlit** integrada ao **Xano (PostgreSQL)** e modelagem relacional das entidades (`User`, `Account`, `Category`, `Transaction`, `Budget`, `Goal`, `AiInsight`) em [`ARCHITECTURE.md`](./ARCHITECTURE.md).
  - [x] Especificação detalhada dos Requisitos Funcionais (`RF01`–`RF12`), Não Funcionais (`RNF01`–`RNF04`) e regras de negócio em [`SPECIFICATION.md`](./SPECIFICATION.md).
  - [x] Registro de *Delta Specs* na pasta [`changes/`](./changes/).

---

## 2. Integração Backend Xano CLI & XanoScript (`changes/002_...`)
- [x] **Fase 2: Infraestrutura Xano e Versionamento `.xs`**
  - [x] Configuração do **Xano CLI** e scaffold da pasta [`xano/`](./xano/).
  - [x] Modelagem em XanoScript (`xano/table/`): `user.xs`, `transacao.xs`, `budget.xs`, `insight.xs`, `event_log.xs`.
  - [x] Grupos de API no Xano (`xano/api/orbitfin/` e `xano/api/authentication/`): endpoints de autenticação, transações, saldo, orçamentos e insights.
  - [x] Configuração de `.gitignore` e `.streamlit/secrets.toml.example`.
  - [x] Camada de serviços modularizada em [`services/`](./services/) (`storage.py`, `api_client.py`, `xano_storage.py`, `sqlite_storage.py`).

---

## 3. Interface Streamlit e Módulos do MVP
- [x] **Fase 3: Autenticação e Painel Principal (Dashboard em Streamlit)**
  - [x] Tela de Login e Cadastro (`app.py` e protótipo de referência em `4/login.html`) seguindo a paleta Terracota (`#E05638`), Azul Marinho (`#1A2238`) e Cinza Claro (`#F4F6F8`).
  - [x] Controle de sessão via token JWT e identificação pelo primeiro nome do usuário.
  - [x] Painel Principal em **Streamlit** com KPIs no topo (**Saldo Total Atual**, **Receitas**, **Despesas**), **Visão Geral do Mês (Donut Chart)**, **Receitas vs. Despesas**, **Limites de Gastos**, **Metas Financeiras** e **Sugestões da IA**.
  - [x] CRUD de transações, categorias/limites e metas financeiras diretamente pelo Streamlit.

---

## 4. Evoluções Futuras e Pós-MVP
- [ ] **Fase 4: Expansão Analítica no Streamlit e Xano**
  - [ ] Expansão do módulo de **Sugestões da IA** no **Streamlit** conectado à tabela `AiInsight` / `insight` do Xano com simulações interativas de economia.
  - [ ] Expansão dos endpoints XanoScript (`PUT /budgets`, `CRUD /account`, `CRUD /goal`) diretamente no grupo `api:orbitfin`.
  - [ ] Importação automatizada de extratos bancários (OFX / CSV) via upload no Streamlit.
  - [ ] Alertas visuais no Streamlit quando um limite de categoria atingir 90% do orçamento mensal.
