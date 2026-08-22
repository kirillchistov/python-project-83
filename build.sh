#!/usr/bin/env bash
# Download uv and install project dependencies (used by render.com).
set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
make install
