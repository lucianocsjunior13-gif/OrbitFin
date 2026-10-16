// Cria transação — RF03
query transacoes verb=POST {
  api_group = "OrbitFin"
  auth = "user"

  input {
    text tipo filters=trim
    decimal valor
    text data filters=trim
    text categoria filters=trim
    text descricao? filters=trim
    text status filters=trim
  }

  stack {
    precondition ($input.tipo == "receita" || $input.tipo == "despesa") {
      error_type = "inputerror"
      error = "tipo deve ser receita ou despesa"
    }
  
    precondition ($input.status == "pago" || $input.status == "pendente") {
      error_type = "inputerror"
      error = "status deve ser pago ou pendente"
    }
  
    precondition ($input.valor > 0) {
      error_type = "inputerror"
      error = "valor deve ser positivo"
    }
  
    db.add transacao {
      data = {
        created_at: "now"
        user_id   : $auth.id
        tipo      : $input.tipo
        valor     : $input.valor
        data      : $input.data
        categoria : $input.categoria
        descricao : $input.descricao
        status    : $input.status
      }
    } as $transacao
  }

  response = $transacao
  guid = "JUseI8eRSikgsyZ7u4hKagLtkOk"
}