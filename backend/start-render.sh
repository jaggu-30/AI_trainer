#!/usr/bin/env sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT_DIR/backend"
export PYTHONPATH="$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"

# Apply the committed schema migrations before serving traffic.  The command
# is idempotent, so restarts and ordinary deployments are safe.
alembic upgrade head

exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-10000}"
