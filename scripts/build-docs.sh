#!/bin/sh
#
# Wrapper for building the docs
set -e
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec uv run --project "$ROOT" --group docs make -C "$ROOT/doc" html
