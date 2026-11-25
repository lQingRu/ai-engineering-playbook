#!/usr/bin/env sh
set -eu
exec "${PYTHON:-python3}" "$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)/playbook.py" install "$@"
