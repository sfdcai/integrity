#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
API_HOST=${API_HOST:-$(hostname -I | awk '{print $1}' || echo "localhost")}
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-5173}
CHECK_FRONTEND=${CHECK_FRONTEND:-1}
LOG_LINES=${LOG_LINES:-120}

log() { printf "[INFO] %s\n" "$*"; }
warn() { printf "[WARN] %s\n" "$*"; }
error() { printf "[ERROR] %s\n" "$*" >&2; }

require_pm2() {
  if ! command -v pm2 >/dev/null 2>&1; then
    error "pm2 is required for health checks. Run scripts/install_ubuntu.sh first.";
    exit 1;
  fi
}

check_backend() {
  local url="http://${API_HOST}:${BACKEND_PORT}"
  if curl -fsS "$url" >/dev/null 2>&1; then
    log "Backend reachable at ${url}"
    return 0
  fi
  warn "Backend not responding at ${url}; restarting via pm2 ..."
  pm2 restart deepguard-backend || true
  sleep 2
  if curl -fsS "$url" >/dev/null 2>&1; then
    log "Backend recovered and is responding at ${url}"
    return 0
  fi
  error "Backend still unreachable at ${url}. Showing pm2 logs:"
  pm2 logs deepguard-backend --lines ${LOG_LINES} || true
  return 1
}

check_frontend() {
  local url="http://${API_HOST}:${FRONTEND_PORT}"
  if [[ "$CHECK_FRONTEND" -ne 1 ]]; then
    log "Skipping frontend check (CHECK_FRONTEND=${CHECK_FRONTEND})."
    return 0
  fi
  if curl -fsS "$url" >/dev/null 2>&1; then
    log "Frontend reachable at ${url}"
    return 0
  fi
  warn "Frontend not responding at ${url}; restarting via pm2 ..."
  pm2 restart deepguard-frontend || true
  sleep 2
  if curl -fsS "$url" >/dev/null 2>&1; then
    log "Frontend recovered and is responding at ${url}"
    return 0
  fi
  error "Frontend still unreachable at ${url}. Showing pm2 logs:"
  pm2 logs deepguard-frontend --lines ${LOG_LINES} || true
  return 1
}

print_status() {
  pm2 status deepguard-backend deepguard-frontend || true
}

main() {
  require_pm2
  print_status
  check_backend
  check_frontend
  log "Health check complete."
}

main "$@"
