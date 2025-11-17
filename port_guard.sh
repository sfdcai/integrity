#!/usr/bin/env bash
set -euo pipefail

if [[ ${DEBUG:-0} -eq 1 ]]; then
  set -x
fi

# Default ports for DB, backend, and frontend
PORTS=(5432 8000 3000)
COMPOSE_ROOT="${COMPOSE_ROOT:-$(pwd)/deepguard-app}"

log() { printf "[INFO] %s\n" "$*"; }
warn() { printf "[WARN] %s\n" "$*"; }
error_exit() { printf "[ERROR] %s\n" "$*" >&2; exit 1; }

usage() {
  cat <<USAGE
Usage: $0 [--compose-root <path>] [--ports "p1 p2 ..."]

Options:
  --compose-root <path>  Path to the docker-compose.yml directory (default: ${COMPOSE_ROOT}).
  --ports "p1 p2 ..."   Space-delimited list of ports to validate (default: ${PORTS[*]}).
  --help                 Show this message.

Environment:
  DEBUG=1                Enable verbose shell tracing for troubleshooting.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --compose-root)
      COMPOSE_ROOT=${2:?"--compose-root requires a value"}; shift 2 ;;
    --ports)
      IFS=' ' read -r -a PORTS <<< "${2:?"--ports requires a value"}"; shift 2 ;;
    --help|-h)
      usage; exit 0 ;;
    *)
      error_exit "Unknown option: $1" ;;
  esac
done

ensure_compose_available() {
  if docker compose version >/dev/null 2>&1; then
    echo "docker compose"
    return 0
  fi
  if command -v docker-compose >/dev/null 2>&1; then
    echo "docker-compose"
    return 0
  fi
  error_exit "Docker Compose not found. Please install Docker and Compose."
}

port_in_use() {
  local port="$1"
  if ss -tuln 2>/dev/null | awk '{print $5}' | grep -E "(^|:)${port}$" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

start_services() {
  local compose_bin
  compose_bin=$(ensure_compose_available)

  if [[ ! -f "$COMPOSE_ROOT/docker-compose.yml" ]]; then
    error_exit "docker-compose.yml not found in ${COMPOSE_ROOT}"
  fi

  log "Starting services via ${compose_bin} in ${COMPOSE_ROOT}"
  (cd "$COMPOSE_ROOT" && ${compose_bin} up -d)
  log "Compose status:"
  (cd "$COMPOSE_ROOT" && ${compose_bin} ps)
}

main() {
  log "Checking ports: ${PORTS[*]}"
  local missing=()
  for port in "${PORTS[@]}"; do
    if port_in_use "$port"; then
      log "Port ${port} is already in use."
    else
      warn "Port ${port} is not listening."
      missing+=("$port")
    fi
  done

  if [[ ${#missing[@]} -eq 0 ]]; then
    log "All monitored ports are active."
    exit 0
  fi

  warn "Detected inactive ports: ${missing[*]}"
  start_services

  log "Rechecking after start..."
  for port in "${missing[@]}"; do
    if port_in_use "$port"; then
      log "Port ${port} is now active."
    else
      warn "Port ${port} is still inactive. Check logs for details."
    fi
  done

  log "Service logs (last 50 lines per container):"
  compose_bin=$(ensure_compose_available)
  (cd "$COMPOSE_ROOT" && ${compose_bin} ps --all)
  (cd "$COMPOSE_ROOT" && ${compose_bin} logs --tail=50)
}

main "$@"
