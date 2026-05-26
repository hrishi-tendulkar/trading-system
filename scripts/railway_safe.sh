#!/usr/bin/env bash
set -euo pipefail

# The local shell may export a stale RAILWAY_TOKEN from ~/.zshrc.
# Unset it so Railway CLI can fall back to the linked local OAuth session.
env -u RAILWAY_TOKEN railway "$@"
