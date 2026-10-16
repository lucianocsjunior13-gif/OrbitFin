// Limite de gasto por categoria, por usuário
table budget {
  auth = false

  schema {
    int id
    timestamp updated_at?=now
  
    // Dono do orçamento
    int user_id {
      table = "user"
    }
  
    text categoria filters=trim
    decimal limite
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {
      type : "btree|unique"
      field: [{name: "user_id", op: "asc"}, {name: "categoria", op: "asc"}]
    }
  ]

  guid = "1T3fxhcA4Pv0u8cro2GDuJZtusg"
}