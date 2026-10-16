# ARCHITECTURE.md: OrbitFin

## Pilha Tecnológica (Tech Stack)
- **Front-end & Interface:** Python + **Streamlit** (responsável por renderizar telas, formulários, gráficos e tabelas reativas).
- **Back-end & Banco de Dados (BaaS):** **Xano** (API RESTful, lógica de negócio, autenticação JWT e banco de dados PostgreSQL gerenciado).
- **Metodologia & Documentação:** **OpenSpec** (padrão em Markdown para rastreabilidade de requisitos, arquitetura e versionamento de mudanças).

## Arquitetura de Comunicação

┌─────────────────────────────────┐
│       Streamlit (Python)        │  <-- Interface do Usuário (Frontend)
│  - Páginas / Componentes UI     │
│  - Requisições HTTP (Requests)  │
└────────────────┬────────────────┘
│
│ REST API (JSON / Bearer Token)
▼
┌─────────────────────────────────┐
│             Xano                │  <-- Backend & Banco de Dados
│  - Endpoints de API / Auth      │
│  - Regras de Negócio / PostgreSQL│
└─────────────────────────────────┘

## Estrutura de Pastas (estado atual)

```
orbitfin/
├── OPENSPEC.md
├── PRODUCT.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── changes/
│   ├── 001_local_storage_implementation.md
│   └── 002_xano_cli_xanoscript_integration.md
├── app.py                      # Entrypoint Streamlit
├── requirements.txt
├── .streamlit/
│   └── secrets.toml.example    # Copiar para secrets.toml (não versionar)
├── xano/                       # Backend versionado (XanoScript + CLI)
│   ├── table/                  # user, transacao, budget, insight, …
│   └── api/orbitfin/           # API Group canonical = orbitfin
└── services/
    ├── storage.py              # Adapter: SQLite local ↔ Xano (flag secrets)
    ├── api_client.py           # HTTP + Bearer para Xano
    ├── xano_storage.py         # Implementação remota
    ├── sqlite_storage.py       # Fallback offline
    └── local_storage.py        # Legado JSON
```

### Dual mode (local vs Xano)

Em `.streamlit/secrets.toml`:

```toml
[xano]
enabled = true   # false = SQLite local
base_url = "https://<instance>.n7.xano.io/api:orbitfin"
```

`app.py` importa apenas `services.storage`, que escolhe o backend.

### URL da API

Base: `https://x8ki-letl-twmt.n7.xano.io/api:orbitfin`  
Paths: `/login`, `/register`, `/transacoes`, `/saldo`, `/budgets`, `/insights`

---


### 3. `SPECIFICATION.md` (Especificação Técnica e Comportamental)

```markdown
# SPECIFICATION.md: OrbitFin

## 1. Requisitos Funcionais (RF)
- **RF01:** O sistema deve permitir que o usuário crie uma conta informando e-mail e senha, salvando os dados de forma segura no Xano.
- **RF02:** O usuário deve conseguir autenticar-se na plataforma, recebendo um token de acesso para consumir as rotas protegidas da API.
- **RF03:** O usuário deve poder registrar uma nova transação (receita ou despesa) informando valor, categoria, data e descrição.
- **RF04:** O Streamlit deve listar todas as transações cadastradas do usuário logado em uma tabela interativa com opções de exclusão e edição.
- **RF05:** O dashboard principal deve exibir gráficos de pizza/barra consolidados por categoria utilizando as bibliotecas nativas do Streamlit integradas aos dados do Xano.

## 2. Requisitos Não Funcionais (RNF)
- **RNF01:** A interface em Streamlit deve carregar as páginas de forma fluida, exibindo indicadores de carregamento (`st.spinner`) durante chamadas assíncronas à API do Xano.
- **RNF02:** As credenciais de acesso e tokens de API devem ser mantidos em variáveis de ambiente seguras (`st.secrets`).
- **RNF03:** O código Python deve seguir as boas práticas de modularização (separando a camada de UI da camada de serviço/API).

---
*(Adicione aqui regras de validação adicionais, ex: valores monetários não podem ser negativos, datas futuras não podem ser marcadas como pagas, etc.)*

