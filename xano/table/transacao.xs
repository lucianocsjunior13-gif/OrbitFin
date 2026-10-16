// Transações financeiras do usuário (receitas e despesas)
table transacao {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // Dono da transação
    int user_id {
      table = "user"
    }
  
    enum tipo {
      values = ["receita", "despesa"]
    }
  
    decimal valor
    date data
    text categoria filters=trim
    text descricao? filters=trim
    enum status {
      values = ["pago", "pendente"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "data", op: "desc"}]}
  ]

  guid = "imydC3MPDmHrykdhqUA_G4xICjM"
}