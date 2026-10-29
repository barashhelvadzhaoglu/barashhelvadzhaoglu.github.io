#!/bin/zsh
# barashhelvadzhaoglu.com: eksik çevirileri Gemini ile tamamla (launchd ile günlük çalışır)
cd "$(dirname "$0")/.." || exit 1
PY=/usr/bin/python3
[ -x "$HOME/lebeninsider/.venv/bin/python3" ] && PY="$HOME/lebeninsider/.venv/bin/python3"
"$PY" -u script/translate_missing.py --limit 10
