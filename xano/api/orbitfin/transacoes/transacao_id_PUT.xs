// Atualiza transação do usuário — RF04
query "transacoes/{transacao_id}" verb=PUT {
  api_group = "OrbitFin"
  auth = "user"

  input {
    int transacao_id
    text tipo filters=trim
    decimal valor
    text data filters=trim
    text categoria filters=trim
    text descricao? filters=trim
    text status filters=trim
  }

  stack {
    db.get transacao {
      field_name = "id"
      field_value = $input.transacao_id
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Transacao nao encontrada"
    }

    precondition ($existente.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Transacao nao pertence ao usuario"
    }

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

    db.edit transacao {
      field_name = "id"
      field_value = $input.transacao_id
      data = {
        tipo     : $input.tipo
        valor    : $input.valor
        data     : $input.data
        categoria: $input.categoria
        descricao: $input.descricao
        status   : $input.status
      }
    } as $transacao
  }

  response = $transacao
  guid = "-in17lmlqKZazstzN-Pw4CNbUk0"
}
