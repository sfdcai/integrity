#!/usr/bin/env bash
set -euo pipefail

# Debug tracing when DEBUG=1
if [[ ${DEBUG:-0} -eq 1 ]]; then
  set -x
fi

RELEASE_TAG="v0.0.01"
USE_LATEST=0
INSTALL_DIR="$(pwd)/integrity"
SKIP_COMPOSE=0
APT_UPDATED=0

log() { printf "[INFO] %s\n" "$*"; }
warn() { printf "[WARN] %s\n" "$*"; }
error_exit() { printf "[ERROR] %s\n" "$*" >&2; exit 1; }

usage() {
  cat <<USAGE
Usage: $0 [--latest] [--release-tag <tag>] [--install-dir <path>] [--skip-compose]

Options:
  --latest              Use the latest GitHub release instead of the default tag (${RELEASE_TAG}).
  --release-tag <tag>   Download a specific release tag (default: ${RELEASE_TAG}).
  --install-dir <path>  Destination directory for the unpacked project (default: ${INSTALL_DIR}).
  --skip-compose        Skip docker compose build during setup.
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
    --skip-compose)
      SKIP_COMPOSE=1; shift ;;
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

ensure_docker_compose() {
  if command -v docker-compose >/dev/null 2>&1; then
    log "docker-compose is available."
    return 0
  fi

  if docker compose version >/dev/null 2>&1; then
    log "Docker Compose plugin is available."
    return 0
  fi

  ensure_apt_updated
  log "Installing Docker Compose plugin..."
  sudo apt-get install -y docker-compose-plugin || sudo apt-get install -y docker-compose
}

start_docker_service() {
  if systemctl is-active --quiet docker; then
    log "Docker service is already running."
    return 0
  fi
  log "Starting Docker service..."
  sudo systemctl enable docker --now || warn "Could not enable/start Docker via systemctl; ensure the daemon is running."
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

compose_build_if_available() {
  local compose_root="$1"
  if [[ ! -d "$compose_root" ]]; then
    warn "Compose directory ${compose_root} not found; skipping docker compose build."
    return 0
  fi
  if [[ $SKIP_COMPOSE -eq 1 ]]; then
    warn "Skipping docker compose build as requested."
    return 0
  fi
  if ! command -v docker >/dev/null 2>&1; then
    warn "Docker not available; skipping compose build."
    return 0
  fi

  start_docker_service
  log "Building containers (this may take several minutes)..."
  (cd "$compose_root" && (docker compose build || docker-compose build))
}

main() {
  log "Beginning installation..."
  ensure_package curl curl
  ensure_package unzip unzip
  ensure_package python3 python3
  ensure_package python3-venv python3
  ensure_package docker docker docker.io
  ensure_docker_compose

  local url
  url=$(determine_download_url)
  download_and_unpack "$url"

  compose_build_if_available "$INSTALL_DIR/deepguard-app"

  log "Installation complete. Project located at ${INSTALL_DIR}".
  log "To start services: cd ${INSTALL_DIR}/deepguard-app && docker compose up -d"
}

main "$@"
