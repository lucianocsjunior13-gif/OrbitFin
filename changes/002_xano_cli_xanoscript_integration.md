# Delta Spec: Integração Xano CLI + XanoScript (backend remoto)

## Objetivo da Mudança
Substituir (ou alternar) o armazenamento local (SQLite/JSON) pelo backend Xano, usando **Xano CLI** para versionar o backend em arquivos **XanoScript (`.xs`)** no repositório, e conectar o Streamlit via `services/api_client.py` com JWT + `st.secrets`.

Esta mudança restaura a arquitetura alvo descrita em `PRODUCT.md` e `ARCHITECTURE.md`: Streamlit (UI) → REST/Bearer → Xano (API + PostgreSQL + Auth).

## Escopo
**Dentro:**
- Setup do Xano CLI e pasta `xano/` com XanoScript versionado em Git
- Schema (tabelas) e endpoints alinhados ao contrato já esperado pelo frontend
- Secrets Streamlit + rewire de `app.py` (ou flag local ↔ Xano)
- Atualização de docs OpenSpec (`ARCHITECTURE.md`, `ROADMAP.md`)

**Fora (por enquanto):**
- Migração de dados SQLite → Xano em massa
- Sandbox/CI avançado (plano pago)
- Features além do MVP (OFX, realtime, etc.)

## Pré-requisitos
1. Conta Xano + workspace criado (ex.: `OrbitFin`)
2. Node.js LTS instalado (necessário para `@xano/cli`)
3. Leitura prévia obrigatória (OpenSpec): `PRODUCT.md`, `ARCHITECTURE.md`, este delta

---

## Passo a passo

### Fase 0 — Alinhamento OpenSpec (antes de qualquer código)
1. Confirmar RFs em `ARCHITECTURE.md` (SPEC embutida): RF01–RF05, RNF01–RNF03.
2. Usar este arquivo (`changes/002_...`) como contrato da entrega.
3. **Não** alterar Python até o backend Xano responder 200 nos endpoints críticos (login + listar transações).

### Fase 1 — Xano CLI no ambiente local
```powershell
# Node (se ainda não tiver)
winget install OpenJS.NodeJS.LTS
# Reabrir o terminal, depois:
npm install -g @xano/cli
xano --version
xano auth
xano profile me
```
- `xano auth` abre o browser; selecionar instance + workspace OrbitFin.
- Credenciais ficam em `~/.xano/credentials.yaml` (não commitar).

### Fase 2 — Scaffold XanoScript no repo
Na raiz do OrbitFin:
```powershell
mkdir xano
xano workspace pull -d ./xano
git add xano
git commit -m "chore: scaffold XanoScript workspace"
```

Estrutura esperada (após evoluir o backend):
```
xano/
├── table/                 # user, transacao, budget, insight
├── api/
│   └── orbitfin/          # api_group + queries (endpoints)
├── function/              # opcional
└── task/                  # opcional
```

**Recomendação leiga:** criar Auth + CRUD primeiro no **builder visual** do Xano → `xano workspace pull -d ./xano` → aprender XanoScript lendo os `.xs` gerados. Depois editar localmente e fazer push.

### Fase 3 — Modelo de dados (tabelas)
Espelhar o contrato local atual (`sqlite_storage` / `api_client`):

| Tabela | Campos mínimos | Notas |
|--------|----------------|-------|
| `user` | `email`, `password`, `name`, `created_at` | `auth = true`; password tipo nativo Xano (hash) |
| `transacao` | `user_id`, `tipo`, `valor`, `data`, `categoria`, `descricao`, `status`, `created_at` | Filtrar sempre por usuário autenticado |
| `budget` | `user_id`, `categoria`, `limite`, `updated_at` | Seed com categorias padrão do app |
| `insight` | `texto`, `created_at` | Opcional no MVP |

### Fase 4 — Endpoints (contrato com o frontend)
Alinhar com `services/api_client.py` e `orbitfin_streamlit.py`.

| Método | Path relativo (após BASE_URL) | Request / Response |
|--------|-------------------------------|--------------------|
| POST | `/login` | body `{email, password}` → `{access_token}` (+ user opcional) |
| POST | `/register` | body `{email, password, name}` → 200/201 |
| GET | `/transacoes` | Bearer → lista |
| POST | `/transacoes` | Bearer + body CRUD |
| PUT | `/transacoes/{id}` | Bearer + body |
| DELETE | `/transacoes/{id}` | Bearer → 200/204 |
| GET | `/saldo` | Bearer → `{valor}` |
| GET | `/budgets` | Bearer → lista com `categoria`, `limite`, `gastoAtual`, `percentual` |
| GET | `/insights` | Bearer → `{texto}` ou lista |

**URL real Xano:** `https://<instance>.xano.io/api:<canonical>/<path>`  
Ex.: canonical do API Group = `orbitfin` →  
`BASE_URL = "https://xxxx.xano.io/api:orbitfin"`  
e o client chama `f"{BASE_URL}/login"`.

**Normalização de token:** Xano costuma devolver `authToken`; o app espera `access_token`. Padronizar **num dos lados** (preferência: response do endpoint = `{access_token}` para não espalhar ifs no Python).

### Fase 5 — Loop CLI (desenvolver backend)
```powershell
# editar .xs em ./xano
xano workspace push -d ./xano --dry-run   # preview, não aplica
xano workspace push -d ./xano             # aplica (plano free: direto no workspace)

# plano pago (quando disponível):
# xano sandbox push -d ./xano
# xano sandbox review
```
Regras:
- Sempre `--dry-run` antes do primeiro push do dia / mudanças de schema
- Commit Git **antes** de push destrutivo
- Evitar `--force`, `--delete`, `--truncate` sem revisão humana

### Fase 6 — Secrets Streamlit
Criar `.streamlit/secrets.toml` (local, **fora do Git**):
```toml
[xano]
base_url = "https://<sua-instance>.xano.io/api:orbitfin"
```

Ajustar `.gitignore` para ignorar:
- `.streamlit/secrets.toml`
- `data/`
- `*.db`
- (corrigir o `.gitignore` atual que está inválido com conteúdo `nul`)

### Fase 7 — Integração Python
1. Em `services/api_client.py`: usar `st.secrets["xano"]["base_url"]`; remover placeholder `localhost:5000` em produção.
2. Garantir que login seta `st.session_state.token` com o Bearer.
3. Rewire de `app.py`:
   - **Opção A (simples):** trocar imports de `sqlite_storage` → wrappers em `api_client`
   - **Opção B (melhor):** flag `USE_XANO` / adapter único (`get_storage()`) local ↔ remoto
4. Preferir `orbitfin_streamlit.py` como referência de fluxo HTTP; unificar num entrypoint só (`app.py`).
5. Manter loading (`st.spinner`) nas chamadas (RNF01).

### Fase 8 — Validação e docs
1. Testar no Swagger/Run do Xano: register → login → CRUD transação → saldo/budgets.
2. Testar Streamlit ponta a ponta.
3. Atualizar:
   - `ROADMAP.md` (marcar fases concluídas)
   - `ARCHITECTURE.md` (estrutura real: pasta `xano/`, SQLite como fallback se mantido)
   - Este delta: checkboxes de aceite

---

## Arquivos Afetados (previsto)

### Novos
- `xano/**/*.xs` — backend versionado (XanoScript)
- `xano/README.md` — (opcional) como puxar/pushar
- `.streamlit/secrets.toml` — **local only**, não versionar
- `changes/002_xano_cli_xanoscript_integration.md` — este documento

### Modificados
- `services/api_client.py` — BASE_URL via secrets; paths alinhados; token
- `app.py` — consumo via API (ou adapter)
- `.gitignore` — secrets, data, db
- `ROADMAP.md`, `ARCHITECTURE.md` — refletir estado real
- `README.md` / `README_LOCAL.md` — dual mode local vs Xano (se mantido)

### Mantidos / referência
- `services/sqlite_storage.py`, `services/local_storage.py` — fallback offline ou remoção futura
- `orbitfin_streamlit.py` — referência de endpoints até unificação

---

## Critérios de Aceite
- [ ] Workspace Xano existe e CLI autentica (`xano profile me` ok)
- [ ] Pasta `xano/` no repo com `.xs` de tables + API Group após pull
- [ ] Push dry-run + push real funcionam sem duplicar objetos
- [ ] `POST register` e `POST login` retornam sucesso; login devolve `access_token`
- [ ] Rotas de `transacoes` exigem Bearer e isolam dados por usuário
- [ ] `GET saldo`, `GET budgets`, `GET insights` batem o shape esperado pelo Streamlit
- [ ] Streamlit autentica via Xano e faz CRUD de transações sem SQLite
- [ ] Secrets só em `st.secrets`; nada de URL/token commitado
- [ ] `.gitignore` corrigido (secrets + data)
- [ ] `ROADMAP.md` / `ARCHITECTURE.md` atualizados
- [ ] OpenSpec respeitado: este delta existia **antes** da implementação Python final

---

## Observações de Implementação
- XanoScript **é** o backend; não há Flask/FastAPI paralelo.
- Plano free: push direto no workspace (`xano workspace push`). Sandbox é plano pago.
- Paths do client hoje usam prefixo `/api/...`; na prática a `BASE_URL` já inclui `api:<canonical>`, então os paths relativos devem ser `/login`, `/transacoes`, etc. — ajustar `api_client` na Fase 7.
- Budgets: ou o endpoint Xano calcula `gastoAtual`/`percentual`, ou o Python continua calculando a partir das transações (como no SQLite).
- Senhas plain text do storage local **não** migram para produção; no Xano usar tipo password nativo.
- Agentes de IA: permitir `push --dry-run`; exigir confirmação humana para `push` real / `--delete` / `--force`.

## Ordem de execução sugerida (checklist curto)
1. [ ] Fase 0 — ler docs OpenSpec
2. [ ] Fase 1 — instalar CLI + auth
3. [ ] Fase 2 — pull scaffold `./xano`
4. [ ] Fase 3–4 — tabelas + endpoints (UI ou `.xs`)
5. [ ] Fase 5 — dry-run / push
6. [ ] Fase 6 — secrets
7. [ ] Fase 7 — Python
8. [ ] Fase 8 — aceite + docs
