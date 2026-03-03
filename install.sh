#!/bin/bash
# BrJoy WebP Optimizer - Installer (Desktop WebView runtime)

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "BrJoy WebP Optimizer - Install"
echo "=============================="

auto_install_python_pkg() {
  local pkg="$1"
  local import_name="$2"

  if python3 -c "import ${import_name}" >/dev/null 2>&1; then
    echo "OK: ${pkg} already installed"
    return
  fi

  read -r -p "Install Python package '${pkg}' now? (y/n) " reply
  if [[ "$reply" =~ ^[Yy]$ ]]; then
    python3 -m pip install --user "$pkg"
    echo "OK: ${pkg} installed"
  else
    echo "SKIP: ${pkg} not installed"
  fi
}

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: Python 3.8+ is required"
  exit 1
fi

echo "OK: $(python3 --version)"

if ! command -v convert >/dev/null 2>&1; then
  echo "WARN: ImageMagick not found"
  read -r -p "Install ImageMagick with apt? (y/n) " reply
  if [[ "$reply" =~ ^[Yy]$ ]]; then
    sudo apt update
    sudo apt install -y imagemagick
  else
    echo "ERROR: ImageMagick is required"
    exit 1
  fi
fi

echo "OK: ImageMagick found"

auto_install_python_pkg "pywebview" "webview"
auto_install_python_pkg "pillow" "PIL"
auto_install_python_pkg "tkinterdnd2" "tkinterdnd2"

if [ ! -f "$ROOT_DIR/frontend/dist/index.html" ]; then
  echo "WARN: frontend bundle not found at frontend/dist/index.html"
  if command -v npm >/dev/null 2>&1; then
    read -r -p "Build frontend bundle now (requires npm registry access)? (y/n) " reply
    if [[ "$reply" =~ ^[Yy]$ ]]; then
      if [ -f "$ROOT_DIR/frontend/package-lock.json" ]; then
        npm ci --prefix "$ROOT_DIR/frontend"
      else
        npm install --prefix "$ROOT_DIR/frontend"
      fi
      npm run build --prefix "$ROOT_DIR/frontend"
      echo "OK: frontend bundle built"
    else
      echo "SKIP: bundle build"
    fi
  else
    echo "SKIP: npm not found (only needed for development/build)"
  fi
else
  echo "OK: frontend bundle exists"
fi

chmod +x "$ROOT_DIR/brjoy-converter"
echo "OK: brjoy-converter is executable"

echo
echo "Install complete"
echo "Run: ./brjoy-converter"
echo "Note: Runtime needs Python + ImageMagick + pywebview. Node is dev/build only."
