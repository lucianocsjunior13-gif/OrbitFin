// Budgets com gastoAtual e percentual (contrato OpenSpec 002)
query budgets verb=GET {
  api_group = "OrbitFin"
  auth = "user"

  input {
  }

  stack {
    db.query budget {
      where = $db.budget.user_id == $auth.id
      sort = {budget.categoria: "asc"}
      return = {type: "list"}
    } as $budgets
  
    db.query transacao {
      where = $db.transacao.user_id == $auth.id && $db.transacao.tipo == "despesa"
      return = {type: "list"}
    } as $despesas
  
    var $resultado {
      value = []
    }
  
    foreach ($budgets) {
      each as $b {
        var $gasto {
          value = 0
        }
      
        foreach ($despesas) {
          each as $d {
            conditional {
              if ($d.categoria == $b.categoria) {
                math.add $gasto {
                  value = $d.valor
                }
              }
            }
          }
        }
      
        var $percentual {
          value = 0
        }
      
        conditional {
          if ($b.limite > 0) {
            var.update $percentual {
              value = ($gasto / $b.limite) * 100
            }
          }
        }
      
        array.push $resultado {
          value = {
            id        : $b.id
            categoria : $b.categoria
            limite    : $b.limite
            gastoAtual: $gasto
            percentual: $percentual
          }
        }
      }
    }
  }

  response = $resultado
  guid = "zr5tj6CiF71mCwKkkDOfDrAIZnA"
}