# OrbitFin — Organizador Financeiro Pessoal (Grupo Marte)

## Sobre o Projeto
O **OrbitFin** é um aplicativo web desenvolvido em **Python (Streamlit)** para ajudar os usuários a organizar e controlar sua vida financeira de forma simples e visual. A plataforma permite cadastrar **receitas, despesas, contas e categorias**, acompanhar o **saldo** e visualizar **gráficos** que mostram para onde o dinheiro está indo.

O usuário também pode definir **limites de gastos por categoria** e **metas financeiras**, acompanhando seu progresso ao longo do tempo. Como diferencial, o aplicativo utiliza **Inteligência Artificial (Sugestões da IA)** para analisar os hábitos financeiros do usuário e fornecer sugestões personalizadas, como identificar categorias com gastos elevados e oportunidades de economia.

O projeto possui um **Dashboard (Painel Principal)** centralizando as principais informações financeiras e integra **frontend e motor analítico em Python (Streamlit)** com **backend, banco de dados relacional e APIs (Xano)**, seguindo a proposta de desenvolvimento colaborativo e de um MVP prevista na disciplina sob a norma **OpenSpec**.

---

## Documentação OpenSpec
- [`OPENSPEC.md`](./OPENSPEC.md) — Protocolo e regras de desenvolvimento OpenSpec.
- [`PRODUCT.md`](./PRODUCT.md) — Visão geral do produto, identidade **Orbit / OrbitFin (Grupo Marte)**, paleta oficial de 3 cores (`#E05638`, `#1A2238`, `#F4F6F8`), guia de ícones (**Flaticon UIcons**) e escopo do MVP.
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — Arquitetura técnica (**Python + Streamlit + Xano**), modelagem relacional do banco de dados e estrutura XanoScript (`xano/`).
- [`SPECIFICATION.md`](./SPECIFICATION.md) — Requisitos Funcionais (`RF01`–`RF12`), Não Funcionais (`RNF01`–`RNF04`) e regras de negócio.
- [`ROADMAP.md`](./ROADMAP.md) — Cronograma de evolução e entregas do MVP.
- [`changes/`](./changes/) — Histórico de *Delta Specs* das implementações:
  - [`001_local_storage_implementation.md`](./changes/001_local_storage_implementation.md)
  - [`002_xano_cli_xanoscript_integration.md`](./changes/002_xano_cli_xanoscript_integration.md)
  - [`003_relatorio_oficial_grupo_marte_openspec.md`](./changes/003_relatorio_oficial_grupo_marte_openspec.md)

---

## Como Executar (Streamlit)

1. Crie e ative o ambiente virtual (opcional) e instale as dependências:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.streamlit/secrets.toml` a partir do exemplo:
   ```powershell
   mkdir .streamlit -Force
   copy secrets.toml.example .streamlit\secrets.toml
   ```
3. Inicie o servidor Streamlit:
   ```powershell
   python -m streamlit run app.py --server.port 8501
   ```
4. Acesse no navegador: **http://localhost:8501**

---

## Backend Xano (Xano CLI & XanoScript)

O diretório [`xano/`](./xano/) contém as tabelas e endpoints versionados em **XanoScript (`.xs`)**:

```powershell
npm install -g @xano/cli
xano auth
xano workspace pull -d ./xano
xano workspace push -d ./xano --dry-run
```
