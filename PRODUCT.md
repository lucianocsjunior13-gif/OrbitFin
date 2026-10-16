# PRODUCT.md: OrbitFin — Organizador Financeiro Pessoal (Grupo Marte)

## Sobre o Projeto
O sistema é um aplicativo web desenvolvido em **Python (Streamlit)** para ajudar os usuários a organizar e controlar sua vida financeira de forma simples e visual. A plataforma permite cadastrar **receitas, despesas, contas e categorias**, acompanhar o **saldo** e visualizar **gráficos** que mostram para onde o dinheiro está indo.

O usuário também pode definir **limites de gastos por categoria** e **metas financeiras**, acompanhando seu progresso ao longo do tempo. Como diferencial, o aplicativo utiliza **Inteligência Artificial (Sugestões da IA)** para analisar os hábitos financeiros do usuário e fornecer sugestões personalizadas, como identificar categorias com gastos elevados e oportunidades de economia.

O projeto possui um **Dashboard (Painel Principal)** centralizando as principais informações financeiras e integra **frontend e motor analítico em Python (Streamlit)** com **backend, banco de dados relacional e APIs (Xano)**, seguindo a proposta de desenvolvimento colaborativo e de um MVP prevista na disciplina sob a metodologia **OpenSpec**.

---

## 1. Identidade e Nomenclatura
O projeto adota como nome principal **Orbit** (ou **OrbitFin** na sua versão comercial/aplicação). A escolha une a essência do **Grupo Marte** à proposta de valor da plataforma financeira:
- **Orbit (Órbita):** Transmite a ideia de controle contínuo e acompanhamento constante das finanças. Ter a vida financeira "em órbita" significa manter gastos e metas sob controle, sem perder o rumo.
- **Conexão Espacial e Tecnológica:** Remete ao ecossistema de Marte, combinando inovação, análise inteligente (IA) e navegação simples para o usuário.
- **OrbitFin:** Variação recomendada para reforçar a categoria do aplicativo (*Finance*) em contextos corporativos e acadêmicos.
- **Símbolo:** Planeta em forma de Pentágono representando o planeta Marte e o laranja/terracota representando a órbita.

---

## 2. Paleta de Cores Oficial e Guia Visual
A identidade visual combina a energia do Planeta Vermelho com a sobriedade necessária para um aplicativo de gestão financeira. **Toda a interface segue estritamente as 3 cores do relatório oficial (+ Branco `#FFFFFF` para superfícies de cards):**

| Cor | Hexadecimal | Função no Sistema | Psicologia e Conceito |
| :--- | :--- | :--- | :--- |
| **Vermelho Marte / Terracota** | `#E05638` | Cor Primária, Destaques, Botões Principais, Alertas e Insights de IA | Conecta diretamente à identidade do Grupo Marte. Traz modernidade, destaque e energia, sem a agressividade de um vermelho puro. |
| **Azul Escuro / Marinho** | `#1A2238` | Cabeçalhos, Menus de Navegação, Textos Principais, Ícones UIcons e Elementos Estáveis | Garante a sensação de segurança, estabilidade, confiança e profissionalismo exigidos por um sistema financeiro. |
| **Cinza Claro / Off-White** | `#F4F6F8` | Fundo da Aplicação, Cards Secundários e Áreas de Leitura | Proporciona alto contraste, leitura limpa e visual leve, evitando a fadiga visual no uso contínuo do dashboard. |

---

## 3. Ícones de Interface e Identificação do Usuário
- **Flaticon UIcons:** Todos os ícones seguem o padrão **Flaticon UIcons** (`https://www.flaticon.com/br/uicons/interface-icons`, classes `fi-rr-*` e `fi-br-*`) em traço minimalista monocromático nas cores **Azul Marinho (`#1A2238`)** e **Terracota (`#E05638`)**.
- **Exibição do Primeiro Nome:** Na barra superior do Dashboard, o perfil exibe o **primeiro nome** cadastrado pelo usuário (`first_name` / primeira palavra de `name` registrada no Xano).

---

## 4. Público-Alvo
- Jovens adultos, estudantes e profissionais que buscam organizar suas finanças pessoais sem depender de planilhas complexas.
- Usuários que desejam monitorar gastos por categoria, estabelecer tetos de orçamento mensal, acompanhar metas de curto/longo prazo e receber recomendações práticas de economia geradas por IA.

---

## 5. Principais Funcionalidades (Escopo MVP)
1. **Autenticação e Gestão de Usuários (Xano Auth):** Cadastro completo (`name`, `first_name`, `last_name`, `cpf`, `phone`, `email`, `password`), login com token JWT e proteção de sessão.
2. **Painel Principal (Dashboard Financeiro Interativo):**
   - **KPIs no Topo:** Saldo Total Atual, Receitas do Mês e Despesas do Mês.
   - **Visão Geral do Mês (Gastos por Categoria):** Gráfico de rosca (*Donut Chart*) detalhando a distribuição das despesas.
   - **Receitas vs. Despesas:** Gráfico comparativo de evolução mensal.
   - **Limites de Gastos e Orçamento Mensal:** Barras de progresso horizontais indicando o consumo de cada categoria frente ao teto definido.
   - **Metas Financeiras:** Acompanhamento visual percentual e monetário dos objetivos financeiros.
   - **Sugestões da IA:** Card inteligente com diagnóstico de hábitos financeiros e cálculo de potencial de economia.
3. **Gestão de Contas e Carteiras (`Account`):** Cadastro e controle de saldo de contas bancárias e carteiras.
4. **Gestão de Transações (`Transaction` & `RecurringTransaction`):** Registro, listagem, filtragem e exclusão de receitas e despesas (pontuais ou recorrentes).
5. **Gestão de Categorias e Limites (`Category` & `Budget`):** Criação de categorias personalizadas e definição de tetos mensais de gastos.
6. **Relatórios Analíticos:** Consolidação de fluxo de caixa, taxa de poupança e evolução mensal.