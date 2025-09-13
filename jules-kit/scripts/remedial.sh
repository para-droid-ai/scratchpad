#!/usr/bin/env bash
set -euo pipefail

# Log wrapper: run a command and tee to error.log
logrun() {
  echo "+ $*"
  "$@" 2>&1 | tee error.log
}

echo "Remedial actions menu (edit as needed):"

echo "1) Git clean reset"
git reset --hard || true
git clean -fdx || true

echo "2) Docker rebuild"
docker compose down -v || true
docker compose up --build -d || true
docker ps || true

echo "3) Python env rebuild"
if command -v python3 >/dev/null 2>&1; then
  rm -rf .venv || true
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -r requirements.txt || true
  pip cache purge || true
fi

echo "4) Node env rebuild"
if command -v npm >/dev/null 2>&1; then
  rm -rf node_modules || true
  npm install || true
  npm cache clean --force || true
fi

echo "5) Environment reset"
exec $SHELL -l
