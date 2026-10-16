# ARCHITECTURE.md: Arquitetura Técnica — OrbitFin (Grupo Marte)

## 1. Pilha Tecnológica (Tech Stack)
- **Front-end, Interface Web e Motor Analítico:** Python + **Streamlit** (`app.py`) + **Plotly** + **Flaticon UIcons** (`@flaticon/flaticon-uicons`), estilizados estritamente com a paleta oficial do Grupo Marte (`#E05638` Terracota, `#1A2238` Azul Marinho, `#F4F6F8` Cinza Claro e `#FFFFFF` Branco).
- **Back-end & Banco de Dados em Nuvem (BaaS):** **Xano** (API RESTful, autenticação JWT, regras de negócio e banco de dados PostgreSQL gerenciado), com versionamento declarativo do backend em **XanoScript (`.xs`)** na pasta `xano/` via **Xano CLI**.
- **Análise Financeira e Sugestões de IA no Streamlit:**
  1. **Processamento Direto no Streamlit (`app.py` e `services/`):** A aplicação em **Streamlit** consulta o histórico de transações, limites de gastos e metas do usuário via API do Xano e consolida os indicadores em tempo real.
  2. **Geração de Insights e Recomendações (`AiInsight` / `insight`):** O motor integrado ao **Streamlit** (junto ao endpoint `/insights` / `/ai_insight` do Xano) analisa os hábitos de consumo por categoria, identifica gastos elevados frente ao orçamento definido e calcula oportunidades práticas de economia mensal e anual, exibidas diretamente no card **Sugestões da IA** do Painel Principal.
- **Metodologia & Documentação:** **OpenSpec** (rastreabilidade de requisitos, arquitetura e *Delta Specs* em `changes/`).

---

## 2. Arquitetura de Comunicação

```text
┌──────────────────────────────────────────────────────────┐
│            Python + Streamlit (app.py & services/)       │  <-- Frontend, Gráficos & Motor de IA
│  • Telas: Login/Cadastro, Dashboard, Transações,         │
│    Contas, Categorias/Limites, Metas e Relatórios        │
│  • Processamento de Sugestões de IA e Indicadores (KPIs) │
│  • Paleta Marte (#E05638, #1A2238, #F4F6F8) + UIcons     │
└────────────────────────────┬─────────────────────────────┘
                             │
                             │ REST API (JSON / JWT Bearer Token)
                             ▼
┌──────────────────────────────────────────────────────────┐
│               Xano Cloud (BaaS + PostgreSQL)             │  <-- Backend & Banco de Dados
│  • Grupo Auth:       /api:FODf7XFO (/auth/login, signup) │
│  • Grupo Financeiro: /api:orbitfin (/transacoes, etc.)   │
│  • Código versionado em ./xano/ via XanoScript (.xs)     │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Modelagem do Banco de Dados Relacional

Para suportar o escopo do **OrbitFin**, a modelagem do banco de dados relacional é dividida em dois blocos principais centrados na entidade `User` (relação `1:N`):

```text
 [ User ] ──1:N──> [ Account ] ──1:N──> [ Transaction ]
   │                                         │
   ├──1:N──> [ Category ] ───────────────────┘
   ├──1:N──> [ Budget ]
   ├──1:N──> [ Goal ]
   ├──1:N──> [ AiInsight ]
   └──1:N──> [ RecurringTransaction ]
```

### 3.1. Núcleo Operacional (Core)
1. **`User` (Usuários):** Armazena as credenciais de acesso e dados de perfil (`id`, `name`, `first_name`, `last_name`, `cpf`, `phone`, `email`, `password`, `created_at`). É a entidade central do sistema; todas as demais tabelas possuem chave estrangeira `user_id` (`1:N`).
2. **`Account` (Contas Financeiras / Carteiras):** Representa onde o dinheiro do usuário está alocado (`id`, `user_id`, `name` — ex: *"Nubank"*, *"Inter"*, *"Carteira"*, `type` — corrente, poupança, dinheiro, `balance_initial`).
3. **`Category` (Categorias):** Organiza e classifica o fluxo financeiro (`id`, `user_id`, `name` — ex: *Alimentação*, *Moradia*, *Lazer*, *Salário*, `type` — *receita* ou *despesa*, `color`, `icon`).
4. **`Transaction` / `transacao` (Transações / Movimentações):** Tabela principal de registros do aplicativo (`id`, `user_id`, `account_id`, `category_id` / `categoria`, `amount` / `valor`, `type` / `tipo`, `date` / `data`, `description` / `descricao`, `status` — *pago* ou *pendente*).
5. **`Budget` (Limites de Gastos):** Permite definir um teto de gastos para categorias específicas dentro de um período (`id`, `user_id`, `category_id` / `categoria`, `amount_limit` / `limite`, `month`, `year`), viabilizando as barras de progresso e alertas de orçamento.

### 3.2. Funcionalidades de Valor (Diferenciais)
6. **`Goal` (Metas Financeiras):** Focada no planejamento de médio e longo prazo (`id`, `user_id`, `name`, `target_amount`, `current_amount`, `deadline` — ex: *"Reserva de Emergência"*, *"Viagem"*).
7. **`AiInsight` / `insight` (Insights da IA):** Armazena e fornece as recomendações e diagnósticos financeiros processados pela aplicação em **Streamlit** e pelo **Xano** (`id`, `user_id`, `type` — *alerta*, *oportunidade*, *elogio*, `content` / `texto`, `is_read`, `created_at`).
8. **`RecurringTransaction` (Transações Recorrentes — Opcional):** Automatiza a criação de despesas ou receitas fixas (como assinaturas de streaming, aluguel e salário).

---

## 4. Grupos de API no Xano (`api:orbitfin` e `api:FODf7XFO`)

O projeto mantém compatibilidade com os dois grupos de API configurados na instância Xano (`https://x8ki-letl-twmt.n7.xano.io`):

### 4.1. Grupo `api:orbitfin` (Versionado em `xano/api/orbitfin/`)
- **Base URL:** `https://x8ki-letl-twmt.n7.xano.io/api:orbitfin`
- **Endpoints XanoScript (`.xs`):**
  - `POST /login` (`login_POST.xs`) e `POST /register` (`register_POST.xs`)
  - `GET /transacoes` (`transacoes_GET.xs`), `POST /transacoes` (`transacoes_POST.xs`), `PUT /transacoes/{id}` (`transacao_id_PUT.xs`), `DELETE /transacoes/{id}` (`transacao_id_DELETE.xs`)
  - `GET /saldo` (`saldo_GET.xs`)
  - `GET /budgets` (`budgets_GET.xs`)
  - `GET /insights` (`insights_GET.xs`)

### 4.2. Grupo `api:FODf7XFO` (Autenticação e Entidades Expandidas)
- **Base URL:** `https://x8ki-letl-twmt.n7.xano.io/api:FODf7XFO`
- **Endpoints:**
  - Autenticação (`xano/api/authentication/`): `POST /auth/login`, `POST /auth/signup` (recebendo `name`, `first_name`, `last_name`, `cpf`, `phone`, `email`, `password`) e `GET /auth/me`.
  - Entidades RESTful: `/account`, `/category`, `/transaction`, `/budget`, `/goal`, `/ai_insight`, `/recurring_transaction`.

---

## 5. Estrutura de Pastas do Repositório

```text
OrbitFin-main/
├── OPENSPEC.md                     # Protocolo e regras OpenSpec
├── PRODUCT.md                      # Visão do produto, identidade Grupo Marte e paleta de 3 cores
├── ARCHITECTURE.md                 # Arquitetura técnica (Streamlit + Xano) e modelagem de dados
├── SPECIFICATION.md                # Requisitos Funcionais (RF) e Não Funcionais (RNF)
├── ROADMAP.md                      # Cronograma de fases e checklist de evolução do MVP
├── README.md                       # Guia rápido de instalação e execução (Streamlit + Xano CLI)
├── changes/                        # Histórico de Delta Specs (OpenSpec)
│   ├── 001_local_storage_implementation.md
│   ├── 002_xano_cli_xanoscript_integration.md
│   └── 003_relatorio_oficial_grupo_marte_openspec.md
├── app.py                          # Entrypoint principal da aplicação Streamlit
├── requirements.txt                # Dependências Python (streamlit, requests, pandas, plotly)
├── secrets.toml.example            # Exemplo de configuração para .streamlit/secrets.toml
├── 4/                              # Protótipo HTML/CSS de inspiração da tela de Login
├── xano/                           # Backend versionado em XanoScript (.xs) via Xano CLI
│   ├── table/                      # Definições de tabelas (user.xs, transacao.xs, budget.xs, insight.xs)
│   ├── api/
│   │   ├── authentication/         # Endpoints de autenticação (/auth/login, /auth/signup, /auth/me)
│   │   └── orbitfin/               # Endpoints financeiros do grupo api:orbitfin
│   └── workspace/                  # Configuração do workspace Xano
└── services/                       # Camada de serviços e integração de dados
    ├── storage.py                  # Adapter unificado (Xano API ↔ Fallback local via st.secrets)
    ├── api_client.py               # Cliente HTTP REST + Bearer Token JWT para o Xano
    ├── xano_storage.py             # Implementação de persistência remota no Xano
    ├── sqlite_storage.py           # Persistência local para modo offline/desenvolvimento
    └── local_storage.py            # Gerenciamento de sessão no Streamlit
```

---

## 6. Configuração de Ambiente (`secrets.toml`)

Em `.streamlit/secrets.toml`:

```toml
[xano]
enabled = true
base_url = "https://x8ki-letl-twmt.n7.xano.io/api:orbitfin"
auth_url = "https://x8ki-letl-twmt.n7.xano.io/api:FODf7XFO"
```
