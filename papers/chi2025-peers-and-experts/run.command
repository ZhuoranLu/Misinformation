#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
export PYTHONHASHSEED=0
export MPLBACKEND=Agg
command -v Rscript >/dev/null || { echo 'Rscript is required to run the original R analysis.'; exit 1; }
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
if ! .venv/bin/python -c 'from importlib.metadata import version; from pathlib import Path; assert all(version(n)==v for n,v in (line.split("==") for line in Path("requirements-lock.txt").read_text().splitlines() if line.strip()))' >/dev/null 2>&1; then
  .venv/bin/python -m pip install -r requirements-lock.txt
fi
.venv/bin/python package_check.py
if [ "${1:-}" = "--check" ]; then
  echo 'Environment and package checks passed.'
  exit 0
fi
.venv/bin/python package_check.py --start
.venv/bin/python analysis.py
Rscript --vanilla analysis.R
.venv/bin/python package_check.py --complete
echo 'Completed: original-code outputs are in results/'
