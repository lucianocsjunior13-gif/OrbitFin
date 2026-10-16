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
