# OPENSPEC.md: Protocolo de Desenvolvimento

Este repositório segue o padrão **OpenSpec**. O objetivo é garantir que qualquer modificação ou nova funcionalidade seja planejada textualmente antes de ser codificada.

## Regras do Protocolo para o Agente / Desenvolvedor:
1. **Consulta Prévia:** Antes de implementar qualquer código em Python ou conectar uma rota do Xano, leia os arquivos `PRODUCT.md`, `ARCHITECTURE.md` e `SPECIFICATION.md` para alinhar o contexto.
2. **Ciclo de Alterações (Delta Specs):** Sempre que for desenvolver uma grande funcionalidade, crie uma pasta `changes/` documentando o objetivo da mudança, os arquivos afetados e os critérios de aceite.
3. **Validação:** Toda nova entrega deve respeitar o escopo definido e atualizar a documentação caso haja mudanças estruturais no projeto.