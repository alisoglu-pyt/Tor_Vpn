#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -d myenv ]; then
  echo "Virtual environment not found. Create it with:"
  echo "  python3 -m venv myenv"
  echo "  myenv/bin/python -m pip install -r requirements.txt"
  exit 1
fi
sudo ./myenv/bin/python gui.py
