# OrbitFin

App de finanças pessoais: **Streamlit** (UI) + **Xano** (API/JWT) ou **SQLite** local.

## Docs OpenSpec
- `PRODUCT.md` / `ARCHITECTURE.md` / `ROADMAP.md` / `OPENSPEC.md`
- Delta Xano: `changes/002_xano_cli_xanoscript_integration.md`

## Rodar (Streamlit)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run app.py
```

Em `secrets.toml`: `enabled = true` usa Xano; `false` usa SQLite.

## Backend Xano (CLI)
```powershell
npm install -g @xano/cli
xano auth
xano workspace pull -d ./xano
xano workspace push -d ./xano --dry-run
```

API Group: `api:orbitfin` — ver `xano/api/orbitfin/`.
