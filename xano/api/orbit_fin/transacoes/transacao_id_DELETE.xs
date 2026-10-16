// Exclui transação do usuário — RF04
query "transacoes/{transacao_id}" verb=DELETE {
  api_group = "OrbitFin"
  auth = "user"

  input {
    int transacao_id
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
  
    db.del transacao {
      field_name = "id"
      field_value = $input.transacao_id
    }
  }

  response = {success: true}
  guid = "1S7IfuIExzpNyO0bgjFcDEtIo24"
}