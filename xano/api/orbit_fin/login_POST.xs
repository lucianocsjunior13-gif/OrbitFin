// Login — retorna access_token (contrato do Streamlit / OpenSpec 002)
query login verb=POST {
  api_group = "OrbitFin"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "created_at", "name", "email", "password"]
    } as $user
  
    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }
  
    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_result
  
    precondition ($pass_result) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
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

  guid = "DXnO9wmkZdXCM9eS6r42CtvJ4Do"
}