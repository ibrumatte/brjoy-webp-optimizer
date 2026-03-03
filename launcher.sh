#!/bin/bash
export GDK_BACKEND=x11
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/brjoy-converter"
