#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"goal\" [--headless] [--max-steps N]" >&2
  exit 1
fi

python -m pip install --upgrade pip
python -m pip install playwright pillow requests
python -m playwright install chromium

python main.py "$@"
