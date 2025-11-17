#!/usr/bin/env bash
set -euo pipefail

if [[ ${DEBUG:-0} -eq 1 ]]; then
  set -x
fi

RELEASE_TAG="v0.0.01"
USE_LATEST=0
INSTALL_DIR="$(pwd)/integrity"
APT_UPDATED=0
DB_NAME="deepguard"
DB_USER="deepguard"
DB_PASSWORD="deepguard"

log() { printf "[INFO] %s\n" "$*"; }
warn() { printf "[WARN] %s\n" "$*"; }
error_exit() { printf "[ERROR] %s\n" "$*" >&2; exit 1; }

usage() {
  cat <<USAGE
Usage: $0 [--latest] [--release-tag <tag>] [--install-dir <path>]

Options:
  --latest              Use the latest GitHub release instead of the default tag (${RELEASE_TAG}).
  --release-tag <tag>   Download a specific release tag (default: ${RELEASE_TAG}).
  --install-dir <path>  Destination directory for the unpacked project (default: ${INSTALL_DIR}).
  --help                Show this help message.

Environment:
  DEBUG=1               Enable verbose shell tracing for troubleshooting.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --latest)
      USE_LATEST=1; shift ;;
    --release-tag)
      RELEASE_TAG=${2:?"--release-tag requires a value"}; shift 2 ;;
    --install-dir)
      INSTALL_DIR=${2:?"--install-dir requires a value"}; shift 2 ;;
    --help|-h)
      usage; exit 0 ;;
    *)
      error_exit "Unknown option: $1" ;;
  esac
done

ensure_apt_updated() {
  if [[ $APT_UPDATED -eq 0 ]]; then
    log "Updating apt package index..."
    sudo apt-get update -y
    APT_UPDATED=1
  fi
}

ensure_package() {
  local pkg_name="$1"; shift
  local check_cmd="$1"; shift
  local apt_pkg="${1:-$pkg_name}"

  if command -v "$check_cmd" >/dev/null 2>&1; then
    log "Dependency '$check_cmd' already installed."
    return 0
  fi

  ensure_apt_updated
  log "Installing missing dependency: ${apt_pkg}"
  sudo apt-get install -y "$apt_pkg"
}

fetch_latest_zip_url() {
  python3 - <<'PY' || exit 1
import json, sys, urllib.request
url = 'https://api.github.com/repos/sfdcai/integrity/releases/latest'
try:
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.load(resp)
    zip_url = data.get('zipball_url')
    if not zip_url:
        raise ValueError('zipball_url missing in response')
    print(zip_url)
except Exception as exc:
    sys.stderr.write(f"Failed to fetch latest release info: {exc}\n")
    sys.exit(1)
PY
}

determine_download_url() {
  if [[ $USE_LATEST -eq 1 ]]; then
    log "Resolving latest release zip URL from GitHub..."
    if latest_url=$(fetch_latest_zip_url); then
      echo "$latest_url"
      return 0
    else
      warn "Falling back to tag ${RELEASE_TAG} after failing to resolve latest release."
    fi
  fi
  echo "https://github.com/sfdcai/integrity/archive/refs/tags/${RELEASE_TAG}.zip"
}

download_and_unpack() {
  local url="$1"
  local tmp_dir
  tmp_dir=$(mktemp -d)
  local zip_path="$tmp_dir/integrity.zip"

  log "Downloading release from $url"
  curl -fL "$url" -o "$zip_path"

  log "Unpacking archive..."
  unzip -q "$zip_path" -d "$tmp_dir"
  local src_dir
  src_dir=$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)
  [[ -d "$src_dir" ]] || error_exit "Could not locate unpacked project directory."

  log "Installing project to ${INSTALL_DIR}"
  rm -rf "$INSTALL_DIR"
  mv "$src_dir" "$INSTALL_DIR"
}

ensure_postgres_service() {
  if systemctl is-active --quiet postgresql; then
    log "PostgreSQL service is active."
    return 0
  fi
  ensure_apt_updated
  log "Starting PostgreSQL service..."
  sudo systemctl enable postgresql --now || warn "Unable to enable/start PostgreSQL via systemctl; please start it manually."
}

provision_database() {
  log "Provisioning PostgreSQL role/database (${DB_USER}/${DB_NAME})..."
  sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}' CREATEDB;"

  sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

  sudo -u postgres psql -c "ALTER USER ${DB_USER} PASSWORD '${DB_PASSWORD}';" >/dev/null
}

setup_backend() {
  local backend_dir="$INSTALL_DIR/deepguard-app/backend"
  log "Setting up backend virtual environment..."
  python3 -m venv "$backend_dir/.venv"
  source "$backend_dir/.venv/bin/activate"
  pip install --upgrade pip
  pip install -r "$backend_dir/requirements.txt"

  local env_file="$backend_dir/.env"
  if [[ ! -f "$env_file" ]]; then
    cat > "$env_file" <<INNER_ENV
DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}
INNER_ENV
  fi

  log "Running Alembic migrations..."
  pushd "$backend_dir" >/dev/null
  alembic upgrade head
  popd >/dev/null
  deactivate || true
}

setup_frontend() {
  local frontend_dir="$INSTALL_DIR/deepguard-app/frontend"
  log "Installing frontend dependencies..."
  pushd "$frontend_dir" >/dev/null
  npm install
  npm run build
  popd >/dev/null
}

main() {
  log "Beginning installation..."
  ensure_package curl curl
  ensure_package unzip unzip
  ensure_package python3 python3
  ensure_package python3-venv python3
  ensure_package build-essential gcc
  ensure_package libpq-dev pg_config
  ensure_package postgresql psql postgresql
  ensure_package postgresql-contrib psql postgresql-contrib
  ensure_package nodejs node nodejs
  ensure_package npm npm

  local url
  url=$(determine_download_url)
  download_and_unpack "$url"

  ensure_postgres_service
  provision_database
  setup_backend
  setup_frontend

  log "Installation complete. Project located at ${INSTALL_DIR}."
  log "Backend env: ${INSTALL_DIR}/deepguard-app/backend/.venv"
  log "Database URL: postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}"
  log "Start services with: ${INSTALL_DIR}/port_guard.sh --project-root ${INSTALL_DIR}/deepguard-app"
}

main "$@"
