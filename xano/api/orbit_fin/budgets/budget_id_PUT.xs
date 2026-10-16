// Atualiza limite de um budget do usuário autenticado
query "budgets/{budget_id}" verb=PUT {
  api_group = "OrbitFin"
  auth = "user"

  input {
    int budget_id
    decimal limite
  }

  stack {
    precondition ($input.limite > 0) {
      error_type = "inputerror"
      error = "limite deve ser positivo"
    }

    db.get budget {
      field_name = "id"
      field_value = $input.budget_id
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Budget nao encontrado"
    }

    precondition ($existente.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Budget nao pertence ao usuario"
    }

    db.edit budget {
      field_name = "id"
      field_value = $input.budget_id
      data = {
        limite    : $input.limite
        updated_at: "now"
      }
    } as $budget
  }

  response = $budget
  guid = "xEa8hKmfa2Kglgq-G82CJkwJwAI"
}
