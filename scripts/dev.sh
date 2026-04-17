#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -x "$ROOT/node_modules/.bin/concurrently" ]]; then
  echo "Run: npm install"
  exit 1
fi

mkdir -p "$ROOT/instance"
if [[ ! -f "$ROOT/.env" ]]; then
  export SQLALCHEMY_DATABASE_URI="sqlite:////${ROOT}/instance/agence.db"
fi

PY="python3"
if [[ -x "$ROOT/venv/bin/python" ]]; then
  PY="$ROOT/venv/bin/python"
fi

"$PY" -c "
from app import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    db.create_all()
"

exec "$ROOT/node_modules/.bin/concurrently" -k -n api,ui -c cyan,magenta \
  "cd \"$ROOT\" && exec \"$PY\" \"$ROOT/run.py\"" \
  "cd \"$ROOT\" && npm run dev -w frontend"
