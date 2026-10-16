# Delta Spec: Implementação de Versão com Armazenamento Local

## Objetivo da Mudança
Criar uma versão do aplicativo OrbitFin que utilize armazenamento local em vez de se conectar ao backend Xano, permitindo que o aplicativo funcione totalmente offline com dados salvos em arquivos JSON.

## Arquivos Afetados
1. **Novos arquivos criados:**
   - `services/local_storage.py` - Serviço de armazenamento local que substitui o api_client.py para operações de dados
   - `app.py` - Aplicativo Streamlit principal que usa o local_storage.py
   - `README_LOCAL.md` - Documentação específica para a versão de armazenamento local
   - `data/` directory - Diretório para armazenamento de arquivos JSON
   - `components/` directory - Diretório para componentes reutilizáveis (vazio inicialmente)
   - `assets/` directory - Diretório para arquivos estáticos
   - `changes/` directory - Este documento (conforme protocolo OpenSpec)

2. **Arquivos modificados:**
   - Nenhum arquivo existente foi modificado - toda a nova funcionalidade foi adicionada como novos arquivos

3. **Arquivos mantidos para compatibilidade:**
   - `services/api_client.py` - Mantido para permitir fácil troca entre versões local e Xano
   - `pages/` directory - Mantido para possível uso futuro ou referência
   - Todos os arquivos de especificação (OPENSPEC.md, PRODUCT.md, ARCHITECTURE.md, etc.)

## Critérios de Aceite
✅ O aplicativo deve iniciar e permitir que usuários se cadastrem e façam login  
✅ Todos os dados de usuários devem serem salvos em `data/users.json`  
✅ Transações devem poder ser adicionadas, listadas, editadas e excluídas, com dados salvos em `data/transactions.json`  
✅ Orçamentos devem ser exibidos e editáveis, com limites salvos em `data/budgets.json`  
✅ Metas de economia devem mostrar progresso baseado nos gastos reais  
✅ Dashboard deve exibir KPIs corretos (saldo, receitas, despesas)  
✅ Gráficos de receitas vs. despesas devem ser gerados corretamente  
✅ Indicadores de limite ultrapassado devem funcionar corretamente  
✅ A interface deve exibir indicadores de carregamento durante operações (quando aplicável)  
✅ O código deve seguir boas práticas de modularização (separação de camadas)  

## Observações de Implementação
- Senhas são armazenadas em texto plano nos arquivos JSON para simplicidade nesta versão de demonstração. Em uma versão de produção, seria necessário usar hash de senhas.
- Todos os IDs são gerados sequencialmente baseado no maior ID existente nos dados.
- Formato de data utilizado: YYYY-MM-DD (ISO 8601 sem timezone) para compatibilidade com pandas datetime.
- A estrutura de dados segue aproximadamente a mesma que seria usada com a API Xano, facilitando uma futura migração.
- O aplicativo automaticamente cria dados de exemplo (orçamentos padrão, insight inicial) quando os arquivos de dados estão vazios.