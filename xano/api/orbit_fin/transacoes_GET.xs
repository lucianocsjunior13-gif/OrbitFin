// Lista transações do usuário autenticado — RF04
query transacoes verb=GET {
  api_group = "OrbitFin"
  auth = "user"

  input {
  }

  stack {
    db.query transacao {
      where = $db.transacao.user_id == $auth.id
      sort = {transacao.data: "desc"}
      return = {type: "list"}
    } as $transacoes
  }

  response = $transacoes
  guid = "xpkNrGaFKtGJkeDOU2dPXZ2etbI"
}