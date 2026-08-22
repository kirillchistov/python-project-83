#!/usr/bin/env bash
# Download uv and install project dependencies (used by render.com).
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null 2>&1 || {
  curl -LsSf https://astral.sh/uv/install.sh | sh
}
# uv installer may put env in either location depending on version
if [ -f "$HOME/.local/bin/env" ]; then
  # shellcheck disable=SC1091
  source "$HOME/.local/bin/env"
fi

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

echo "node: $(command -v node) $(node --version)"
echo "npm: $(command -v npm) $(npm --version)"
echo "uv: $(command -v uv) $(uv --version)"

# Render sets NODE_ENV=production and would skip CSS toolchain otherwise.
export NPM_CONFIG_PRODUCTION=false
export NODE_ENV=development

make build-css
make install

# uv may install a non-editable wheel; copy CSS into the package Flask serves.
uv run python - <<'PY'
from pathlib import Path

import page_analyzer

src = Path("page_analyzer/static/style.css").resolve()
dst = Path(page_analyzer.__file__).resolve().parent / "static" / "style.css"
print(f"compiled CSS: {src} exists={src.exists()}")
print(f"package CSS: {dst} exists={dst.exists()}")
if not src.exists():
    raise SystemExit("style.css was not compiled")
if src != dst:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    print(f"copied CSS to {dst}")
PY
