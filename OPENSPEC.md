# OPENSPEC.md: Protocolo de Desenvolvimento — OrbitFin (Grupo Marte)

Este repositório segue rigorosamente o padrão **OpenSpec**. O objetivo é garantir que toda modificação arquitetural, visual ou funcional seja especificada, rastreável e validada antes e durante a codificação.

---

## 1. Pilares da Documentação OpenSpec
1. **[`PRODUCT.md`](./PRODUCT.md):** Visão geral do produto, texto oficial *"Sobre o Projeto"*, identidade e nomenclatura (**Orbit / OrbitFin — Grupo Marte**), paleta oficial de 3 cores, guia de ícones (**Flaticon UIcons**) e escopo do MVP.
2. **[`ARCHITECTURE.md`](./ARCHITECTURE.md):** Pilha tecnológica (**Python + Streamlit** para interface, lógica analítica e insights de IA, e **Xano BaaS + XanoScript CLI** para backend e banco de dados), estrutura de pastas, grupos de API (`api:orbitfin` e `api:FODf7XFO`) e modelagem completa do banco de dados relacional.
3. **[`SPECIFICATION.md`](./SPECIFICATION.md):** Requisitos Funcionais (`RF01` a `RF12`), Requisitos Não Funcionais (`RNF01` a `RNF04`) e contratos de API/dados.
4. **[`ROADMAP.md`](./ROADMAP.md):** Fases de evolução incremental do MVP, integração Xano CLI e entregas concluídas.
5. **[`changes/`](./changes/):** Histórico de *Delta Specs* documentando o objetivo de cada grande entrega, arquivos afetados e critérios de aceite.

---

## 2. Regras do Protocolo para o Agente / Desenvolvedor
1. **Consulta Prévia Obrigatória:** Antes de implementar qualquer código em Python (`app.py`, `services/`) ou alterar rotas/tabelas no Xano (`xano/`), consulte `PRODUCT.md`, `ARCHITECTURE.md` e `SPECIFICATION.md` para manter total alinhamento.
2. **Fidelidade Visual ao Relatório Oficial (Grupo Marte):**
   - Utilizar estritamente as **3 cores oficiais do relatório** (+ Branco `#FFFFFF` para superfícies de cards):
     - **Vermelho Marte / Terracota (`#E05638`):** Cor primária, destaques, botões principais, alertas e insights de IA.
     - **Azul Escuro / Marinho (`#1A2238`):** Cabeçalhos, menus de navegação, textos principais e elementos estáveis.
     - **Cinza Claro / Off-White (`#F4F6F8`):** Fundo da aplicação, cards secundários e áreas de leitura.
   - Utilizar ícones de interface minimalistas do **Flaticon UIcons** (`fi-rr-*` / `fi-br-*`).
3. **Ciclo de Alterações (Delta Specs):** Sempre que desenvolver uma funcionalidade relevante ou evolução de arquitetura, registre um novo arquivo em `changes/` detalhando objetivo, escopo, arquivos afetados e critérios de aceite.
4. **Validação Contínua:** Toda entrega deve respeitar os Requisitos Funcionais e Não Funcionais de `SPECIFICATION.md` e manter a documentação sincronizada com o estado real do código.