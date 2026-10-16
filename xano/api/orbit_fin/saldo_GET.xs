// Saldo = receitas - despesas do usuário autenticado
query saldo verb=GET {
  api_group = "OrbitFin"
  auth = "user"

  input {
  }

  stack {
    db.query transacao {
      where = $db.transacao.user_id == $auth.id && $db.transacao.tipo == "receita"
      return = {type: "list"}
    } as $receitas
  
    db.query transacao {
      where = $db.transacao.user_id == $auth.id && $db.transacao.tipo == "despesa"
      return = {type: "list"}
    } as $despesas
  
    var $total_receitas {
      value = ($receitas|map:$$.valor)|sum
    }
  
    var $total_despesas {
      value = ($despesas|map:$$.valor)|sum
    }
  
    var $saldo {
      value = $total_receitas - $total_despesas
    }
  }

  response = {valor: $saldo}
  guid = "X4L0LwQFQ0BjgTtXJwhxMC5yKdU"
}