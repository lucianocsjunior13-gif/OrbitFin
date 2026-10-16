// Insight / mensagem financeira exibida no dashboard
table insight {
  auth = false

  schema {
    int id
    timestamp updated_at?=now
  
    // Dono do insight (cada usuário tem o seu)
    int user_id {
      table = "user"
    }
  
    text texto filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]

  guid = "DZQidVmq2xzJMSFASFiB0NzIbds"
}