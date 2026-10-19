#!/bin/sh
set -e

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to set up the development environment." >&2
  echo "Install it from https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

if ! command -v gcc >/dev/null 2>&1; then
  echo "WARNING: gcc not found; if a dependency needs to be built," >&2
  echo "install the build tools with: sudo apt install build-essential" >&2
fi

# an editable install puts src/ on sys.path, so a leftover egg-info there is
# found as a second distribution and keeps removed entry points registered
rm -rf chatmaild/src/*.egg-info cmdeploy/src/*.egg-info

uv sync --all-groups
