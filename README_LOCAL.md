# OrbitFin - Controle Financeiro Pessoal (Versão com Armazenamento Local)

Esta é uma versão do aplicativo OrbitFin que utiliza armazenamento local em vez de se conectar ao backend Xano. Todos os dados são salvos em arquivos JSON no diretório `data/`.

## Estrutura do Projeto

```
orbitfin/
├── app.py                  # Arquivo principal do Streamlit
├── requirements.txt        # Dependências Python
├── OPENSPEC.md             # Protocolo de desenvolvimento
├── PRODUCT.md              # Visão do produto
├── ARCHITECTURE.md         # Arquitetura técnica
├── SPECIFICATION.md        # Especificações (vazio)
├── ROADMAP.md              # Plano de desenvolvimento
├── data/                   # Diretório para armazenamento local de dados
│   ├── users.json          # Dados dos usuários
│   ├── transactions.json   # Transações financeiras
│   ├── budgets.json        # Limites de orçamento por categoria
│   └── insights.json       # Mensagens de insight e orientação
├── pages/                  # Páginas do Streamlit (mantido para compatibilidade)
│   ├── 1_Dashboard.py
│   ├── 2_Transacoes.py
│   ├── 3_Orçamento.py
│   └── 4_Metas.py
├── components/             # Componentes reutilizáveis (vazio inicialmente)
├── assets/                 # Arquivos estáticos (imagens, CSS, etc.)
└── services/               # Lógica de serviço
    ├── api_client.py       # Cliente para API Xano (versão original)
    └── local_storage.py    # Serviço de armazenamento local (esta versão)
```

## Como Executar

1. Certifique-se de ter o Python 3.8+ instalado
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```
4. Acesse no navegador: http://localhost:8501

## Funcionalidades

Esta versão inclui todas as funcionalidades do MVP descritas no PRODUCT.md:

1. **Autenticação e Gestão de Usuários**: Cadastro, login seguro e controle de sessão
2. **Dashboard Financeiro Interativo**: 
   - Gráficos dinâmicos de receitas vs. despesas mensais
   - Indicadores visuais (KPIs) de saldo atual, total gasto e receitas do mês
3. **Gestão de Transações**:
   - Cadastro de receitas e despesas com campos como: valor, data, categoria, descrição e status (pago/pendente)
   - Filtros por período, tipo de transação e categoria
   - Edição e exclusão de transações
4. **Categorização de Gastos**:
   - Categorias predefinidas com opção de visualização de gastos vs. limites
   - Alertas quando limites são ultrapassados
5. **Metas de Economia**:
   - Visualização do progresso hacia metas de economia por categoria
   - Alertas quando metas são atingidas

## Armazenamento Local

Os dados são armazenados em formato JSON no diretório `data/`:
- `users.json`: Informações dos usuários (e-mail, nome, etc.)
- `transactions.json`: Todas as transações financeiras
- `budgets.json`: Limites de orçamento definidos por categoria
- `insights.json`: Mensagens de orientação e dicas financeiras

Esta versão é ideal para teste, aprendizado ou uso individual sem necessidade de configuração de backend externo.