#!/usr/bin/env bash
# Download uv and install project dependencies (used by render.com).
set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

if ! command -v npm >/dev/null 2>&1; then
  NODE_VERSION="v22.19.0"
  ARCH="$(uname -m)"
  case "$ARCH" in
    x86_64) NODE_ARCH="x64" ;;
    aarch64|arm64) NODE_ARCH="arm64" ;;
    *)
      echo "Unsupported architecture: $ARCH" >&2
      exit 1
      ;;
  esac
  curl -fsSL "https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz" \
    | tar -xJ -C "$HOME"
  export PATH="$HOME/node-${NODE_VERSION}-linux-${NODE_ARCH}/bin:$PATH"
fi

make install
make build-css
