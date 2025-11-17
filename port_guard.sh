#!/usr/bin/env bash
set -euo pipefail

if [[ ${DEBUG:-0} -eq 1 ]]; then
  set -x
fi

PORTS=(5432 8000 3000)
DB_PORT=5432
BACKEND_PORT=8000
FRONTEND_PORT=3000
PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)/deepguard-app}"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
LOG_DIR="$PROJECT_ROOT/logs"

log() { printf "[INFO] %s\n" "$*"; }
warn() { printf "[WARN] %s\n" "$*"; }
error_exit() { printf "[ERROR] %s\n" "$*" >&2; exit 1; }

usage() {
  cat <<USAGE
Usage: $0 [--project-root <path>] [--ports "p1 p2 p3"]

Options:
  --project-root <path>  Root of the DeepGuard project (default: ${PROJECT_ROOT}).
  --ports "p1 p2 p3"     Space-delimited list of ports (db backend frontend). Default: ${PORTS[*]}.
  --help                 Show this message.

Environment:
  DEBUG=1                Enable verbose shell tracing for troubleshooting.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root)
      PROJECT_ROOT=${2:?"--project-root requires a value"}; BACKEND_DIR="$PROJECT_ROOT/backend"; FRONTEND_DIR="$PROJECT_ROOT/frontend"; LOG_DIR="$PROJECT_ROOT/logs"; shift 2 ;;
    --ports)
      IFS=' ' read -r -a PORTS <<< "${2:?"--ports requires a value"}"; \
      DB_PORT=${PORTS[0]:-$DB_PORT}; BACKEND_PORT=${PORTS[1]:-$BACKEND_PORT}; FRONTEND_PORT=${PORTS[2]:-$FRONTEND_PORT}; shift 2 ;;
    --help|-h)
      usage; exit 0 ;;
    *)
      error_exit "Unknown option: $1" ;;
  esac
done

port_in_use() {
  local port="$1"
  if ss -tuln 2>/dev/null | awk '{print $5}' | grep -E "(^|:)${port}$" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

ensure_log_dir() {
  mkdir -p "$LOG_DIR"
}

ensure_postgres_running() {
  if command -v pg_isready >/dev/null 2>&1 && pg_isready -q -p "$DB_PORT"; then
    log "PostgreSQL already responding on port ${DB_PORT}."
    return 0
  fi
  warn "PostgreSQL not responding on port ${DB_PORT}; attempting to start service..."
  sudo systemctl enable postgresql --now || warn "Could not start PostgreSQL via systemctl; please start it manually."
  sleep 2
  if command -v pg_isready >/dev/null 2>&1 && pg_isready -q -p "$DB_PORT"; then
    log "PostgreSQL is now responding on port ${DB_PORT}."
  else
    warn "PostgreSQL still not responding on port ${DB_PORT}."
  fi
}

start_backend() {
  if port_in_use "$BACKEND_PORT"; then
    log "Backend already listening on ${BACKEND_PORT}."
    return 0
  fi
  if [[ ! -x "$BACKEND_DIR/.venv/bin/uvicorn" ]]; then
    warn "Backend virtualenv not found at $BACKEND_DIR/.venv; run installer first."
    return 1
  fi
  ensure_log_dir
  pushd "$BACKEND_DIR" >/dev/null
  nohup "$BACKEND_DIR/.venv/bin/uvicorn" app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --log-level info > "$LOG_DIR/backend.log" 2>&1 &
  echo $! > "$LOG_DIR/backend.pid"
  popd >/dev/null
  log "Started backend (PID $(cat "$LOG_DIR/backend.pid")) on port ${BACKEND_PORT}. Logs: $LOG_DIR/backend.log"
}

start_frontend() {
  if port_in_use "$FRONTEND_PORT"; then
    log "Frontend already listening on ${FRONTEND_PORT}."
    return 0
  fi
  if [[ ! -f "$FRONTEND_DIR/package.json" ]]; then
    warn "Frontend directory not found at $FRONTEND_DIR; run installer first."
    return 1
  fi
  ensure_log_dir
  pushd "$FRONTEND_DIR" >/dev/null
  nohup npm run dev -- --host --port "$FRONTEND_PORT" > "$LOG_DIR/frontend.log" 2>&1 &
  echo $! > "$LOG_DIR/frontend.pid"
  popd >/dev/null
  log "Started frontend (PID $(cat "$LOG_DIR/frontend.pid")) on port ${FRONTEND_PORT}. Logs: $LOG_DIR/frontend.log"
}

print_status() {
  log "Current port status:"
  for port in "${PORTS[@]}"; do
    if port_in_use "$port"; then
      log "  port ${port}: ACTIVE"
    else
      warn "  port ${port}: inactive"
    fi
  done
  if [[ -f "$LOG_DIR/backend.log" ]]; then
    log "Tail backend log:"; tail -n 20 "$LOG_DIR/backend.log" || true
  fi
  if [[ -f "$LOG_DIR/frontend.log" ]]; then
    log "Tail frontend log:"; tail -n 20 "$LOG_DIR/frontend.log" || true
  fi
}

main() {
  ensure_log_dir
  print_status

  ensure_postgres_running
  start_backend || true
  start_frontend || true

  print_status
}

main "$@"
