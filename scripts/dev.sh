#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p "$ROOT/instance"
if [[ ! -f "$ROOT/.env" ]]; then
  export SQLALCHEMY_DATABASE_URI="sqlite:////${ROOT}/instance/transport.db"
fi

PY="python3"
if [[ -x "$ROOT/venv/bin/python" ]]; then
  PY="$ROOT/venv/bin/python"
fi

"$PY" -c "
from app import create_app
from app.extensions import db
from app.seed import seed_demo_users
app = create_app()
with app.app_context():
    db.create_all()
    seed_demo_users()
"

exec "$PY" "$ROOT/run.py"
