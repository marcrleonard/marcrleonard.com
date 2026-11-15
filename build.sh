#!/usr/bin/env bash
# Cloudflare Pages build command: ./build.sh
# Installs uv if the build image doesn't have it, then builds the site.
# uv downloads a prebuilt Python (see requires-python in pyproject.toml),
# so nothing is compiled from source.
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
	curl -LsSf https://astral.sh/uv/0.13.0/install.sh | sh
	export PATH="$HOME/.local/bin:$PATH"
fi

uv run --locked main.py
