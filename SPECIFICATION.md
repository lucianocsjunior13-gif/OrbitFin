# SPECIFICATION.md: Especificação Técnica e Comportamental — OrbitFin

## 1. Requisitos Funcionais (RF)

### 1.1. Autenticação e Perfil (`User`)
- **RF01 — Cadastro de Usuário no Xano:** O sistema deve permitir que o usuário crie uma conta informando nome (`first_name`, `last_name` e `name`), CPF, telefone, e-mail e senha, gravando os dados de forma segura na tabela `user` do Xano (`/auth/signup` ou `/register`).
- **RF02 — Login e Sessão Autenticada (JWT):** O usuário deve conseguir autenticar-se na plataforma (`/auth/login` ou `/login`), recebendo um token JWT (`authToken` / `access_token`) armazenado em `st.session_state` para consumir as rotas protegidas da API.
- **RF03 — Identificação pelo Primeiro Nome:** A interface deve exibir no cabeçalho do Painel Principal o **primeiro nome** informado pelo usuário no cadastro (`first_name` ou primeira palavra de `name` obtida via `/auth/me`).
- **RF04 — Tela de Login Fiel ao Protótipo (`4/login.html`):** Apresentar card branco centralizado sobre fundo Cinza Claro (`#F4F6F8`), título **OrbitFin** em Vermelho Marte / Terracota (`#E05638`), subtítulo *"Acesse sua conta financeira"*, campos de E-mail e Senha, botão primário **Entrar** em Terracota e alternador **"Não tem conta? Criar conta"**.

### 1.2. Painel Principal (Dashboard — `app.py`)
- **RF05 — Barra Lateral de Navegação e Resumo de Contas:** A barra lateral deve apresentar a identidade **OrbitFin**, os links de navegação com ícones **Flaticon UIcons** (**Dashboard**, **Transações**, **Contas**, **Categorias**, **Metas**, **Relatórios**), o resumo de contas bancárias cadastradas e o botão de ação rápida **`+ Nova Transação`**.
- **RF06 — Indicadores Financeiros (KPIs) no Topo:** Exibir 3 cards principais no topo do Dashboard:
  1. **Saldo Total Atual** (consolidado das contas / fluxo de caixa).
  2. **Receitas** (total de entradas do período).
  3. **Despesas** (total de saídas do período em destaque Terracota `#E05638`).
- **RF07 — Visão Geral do Mês (Gastos por Categoria):** Exibir gráfico de rosca (*Donut Chart*) agrupando as despesas do usuário por categoria.
- **RF08 — Evolução de Receitas vs. Despesas:** Exibir gráfico comparativo mensal entre Receitas (`#1A2238`) e Despesas (`#E05638`).
- **RF09 — Limites de Gastos por Categoria (`Budget`) e Metas Financeiras (`Goal`):** Exibir barras de progresso horizontais demonstrando o valor gasto em relação ao limite mensal de cada categoria (`gasto / limite R$`) e o percentual de conclusão das metas financeiras (`valor_atual / valor_alvo R$`).
- **RF10 — Sugestões da IA (`AiInsight` / Streamlit):** Exibir o card **"Sugestões da IA"** com ícone de lâmpada (`fi-rr-bulb`), apresentando insights processados diretamente no **Streamlit** em integração com a tabela `AiInsight` / `insight` do **Xano**, identificando categorias de maior gasto e calculando a estimativa de economia mensal e anual.

### 1.3. Módulos Operacionais (CRUD)
- **RF11 — Gestão de Transações (`Transaction`):** Permitir registrar, listar, filtrar (por período, tipo, conta e categoria), editar e excluir receitas e despesas informando valor, data, categoria, conta, descrição e status (*pago* ou *pendente*).
- **RF12 — Gestão de Contas (`Account`), Categorias (`Category`), Limites (`Budget`) e Metas (`Goal`):** Permitir cadastrar, atualizar e remover contas financeiras, categorias com orçamento mensal e metas financeiras, sincronizando os dados por usuário (`user_id`).

---

## 2. Requisitos Não Funcionais (RNF)
- **RNF01 — Fidelidade à Paleta Oficial de 3 Cores e Flaticon UIcons:** Toda a interface em Streamlit deve utilizar exclusivamente as cores especificadas no relatório oficial do **Grupo Marte**:
  - **Vermelho Marte / Terracota (`#E05638`)**
  - **Azul Escuro / Marinho (`#1A2238`)**
  - **Cinza Claro / Off-White (`#F4F6F8`)** + `#FFFFFF` para superfícies de cards.
  - Ícones vetoriais **Flaticon UIcons** (`fi-rr-*` / `fi-br-*`) em substituição a emojis coloridos.
- **RNF02 — Fluidez e Feedback Visual:** A interface em Streamlit deve carregar de forma responsiva, exibindo indicadores de carregamento (`st.spinner`) durante chamadas HTTP à API do Xano.
- **RNF03 — Segurança e Segredos (`st.secrets`):** Credenciais sensíveis, URLs configuráveis e tokens de API devem ser gerenciados via `.streamlit/secrets.toml` (ignorado pelo Git, com `secrets.toml.example` versionado) e cabeçalhos `Authorization: Bearer <token>`.
- **RNF04 — Modularização e Backend Versionado (XanoScript):** Separação estrita entre camada de interface (`app.py`), camada de serviços (`services/`) e definições declarativas do backend Xano (`xano/table/*.xs` e `xano/api/**/*.xs`).

---

## 3. Regras de Validação e Negócio
1. **Isolamento por Usuário (`user_id`):** Todo registro de conta, categoria, transação, limite, meta ou insight pertence exclusivamente ao usuário autenticado.
2. **Validação de Valores Monetários:** Valores de transações, limites e metas devem ser numéricos positivos (`> 0`), sendo o impacto no saldo determinado pelo campo `type` (`receita` soma ao saldo; `despesa` subtrai do saldo quando `status == "pago"`).
3. **Integridade no Cadastro de Usuário:** Na criação de conta no Xano, o payload deve preencher tanto `first_name` e `last_name` quanto o campo consolidado `name`, garantindo que nenhuma coluna de identificação fique vazia no banco de dados.
