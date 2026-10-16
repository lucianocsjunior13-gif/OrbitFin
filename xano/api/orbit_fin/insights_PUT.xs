// Atualiza (ou cria) o insight do usuário autenticado
query insights verb=PUT {
  api_group = "OrbitFin"
  auth = "user"

  input {
    text texto filters=trim
  }

  stack {
    precondition (($input.texto|strlen) > 0) {
      error_type = "inputerror"
      error = "texto obrigatorio"
    }

    db.query insight {
      where = $db.insight.user_id == $auth.id
      sort = {insight.id: "desc"}
      return = {type: "list", paging: {page: 1, per_page: 1}}
    } as $existentes

    var $insight {
      value = null
    }

    conditional {
      if (($existentes|count) > 0) {
        db.edit insight {
          field_name = "id"
          field_value = $existentes[0].id
          data = {
            texto     : $input.texto
            updated_at: "now"
          }
        } as $insight
      }
      else {
        db.add insight {
          data = {
            user_id   : $auth.id
            texto     : $input.texto
            updated_at: "now"
          }
        } as $insight
      }
    }
  }

  response = {texto: $insight.texto}
  guid = "NqKWpwGpYGLfrqCWxpk1tpMAMPI"
}
