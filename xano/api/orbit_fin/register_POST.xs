// Cadastro — RF01 / OpenSpec 002
query register verb=POST {
  api_group = "OrbitFin"

  input {
    text name filters=trim
    email email filters=trim|lower
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $existing

    precondition ($existing == null) {
      error_type = "inputerror"
      error = "An account with this email already exists."
    }

    db.add user {
      data = {
        created_at: "now"
        name      : $input.name
        email     : $input.email
        password  : $input.password
        role      : "member"
      }
    } as $user

    // Budgets padrão (mesmo set do sqlite_storage)
    var $defaults {
      value = [
        {categoria: "Alimentação", limite: 800}
        {categoria: "Moradia", limite: 1200}
        {categoria: "Transporte", limite: 400}
        {categoria: "Lazer", limite: 300}
        {categoria: "Saúde", limite: 200}
        {categoria: "Educação", limite: 150}
        {categoria: "Outros", limite: 500}
      ]
    }

    foreach ($defaults) {
      each as $b {
        db.add budget {
          data = {
            user_id   : $user.id
            categoria : $b.categoria
            limite    : $b.limite
            updated_at: "now"
          }
        }
      }
    }

    db.add insight {
      data = {
        user_id   : $user.id
        texto     : "Comece registrando suas transações diárias para ter um melhor controle financeiro."
        updated_at: "now"
      }
    }

    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {
    access_token: $authToken
    user_id     : $user.id
    name        : $user.name
    email       : $user.email
  }
  guid = "ia4XfQj7Y6Tna8XomScNJo1Iz28"
}
