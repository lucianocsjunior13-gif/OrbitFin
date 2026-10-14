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

## Estrutura de Pastas Sugerida

orbitfin/
├── OPENSPEC.md
├── PRODUCT.md
├── ARCHITECTURE.md
├── SPECIFICATION.md
├── ROADMAP.md
├── app.py                  # Arquivo principal do Streamlit
├── requirements.txt        # Dependências Python (streamlit, requests, pandas, etc.)
├── pages/                  # Múltiplas páginas do Streamlit (se aplicável)
│   ├── 1_Dashboard.py
│   ├── 2_Transacoes.py
│   └── 3_Metas.py
└── services/
    └── api_client.py       # Funções de integração com os endpoints do Xano
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

