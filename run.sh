#!/usr/bin/env bash
set -euo pipefail

# Local development runner: sets up the virtualenv, installs pinned
# dependencies, and starts the API with autoreload.
#
# Usage:
#   ./run.sh                # run on port 8000 (or $PORT from .env / environment)
#   PORT=9000 ./run.sh      # override the port
#   ./run.sh --no-reload    # start without uvicorn autoreload

cd "$(dirname "$0")"

VENV_DIR="venv"
PYTHON="${PYTHON:-python3}"

# Load PORT/APP_ENV from .env if present (does not override values already set).
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi
PORT="${PORT:-8000}"

RELOAD_FLAG="--reload"
if [ "${1:-}" = "--no-reload" ]; then
  RELOAD_FLAG=""
fi

if [ ! -d "${VENV_DIR}" ]; then
  echo "==> Creating virtualenv (${VENV_DIR})"
  "${PYTHON}" -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
. "${VENV_DIR}/bin/activate"

echo "==> Installing dependencies from requirements.txt"
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "==> Starting API on http://localhost:${PORT}  (docs: /docs, health: /health)"
exec uvicorn app.main:app ${RELOAD_FLAG} --port "${PORT}"
