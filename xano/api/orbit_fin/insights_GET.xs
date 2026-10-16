// Insight mais recente do usuário
query insights verb=GET {
  api_group = "OrbitFin"
  auth = "user"

  input {
  }

  stack {
    db.query insight {
      where = $db.insight.user_id == $auth.id
      sort = {insight.id: "desc"}
      return = {type: "list", paging: {page: 1, per_page: 1}}
    } as $insights
  
    var $texto {
      value = "Nenhum insight disponivel ainda."
    }
  
    conditional {
      if (($insights|count) > 0) {
        var.update $texto {
          value = $insights[0].texto
        }
      }
    }
  }

  response = {texto: $texto}
  guid = "AEd-UusqJZqkTsgobPhpte5oQRs"
}