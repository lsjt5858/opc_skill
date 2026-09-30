#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir/.." rev-parse --show-toplevel)"

usage() {
  printf 'Usage: %s [--execute]\n' "${0##*/}"
  printf '  no option   Preview configured submodules without changing them.\n'
  printf '  --execute   Sync URLs and update every submodule recursively.\n'
}

execute=false

case "${1:-}" in
  "")
    ;;
  --execute)
    execute=true
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

if [[ $# -gt 1 ]]; then
  usage >&2
  exit 2
fi

if [[ ! -f "$repo_root/.gitmodules" ]]; then
  printf 'No submodules are configured in %s.\n' "$repo_root"
  exit 0
fi

if [[ "$execute" == false ]]; then
  printf '[dry-run] Submodules configured in %s:\n' "$repo_root"
  git -C "$repo_root" submodule status --recursive
  printf '[dry-run] Run %s --execute to sync and update them.\n' "$0"
  exit 0
fi

printf 'Checking submodules for local changes...\n'
git -C "$repo_root" submodule foreach --quiet --recursive '
  if test -n "$(git status --porcelain --untracked-files=normal)"; then
    printf "Refusing to update dirty submodule: %s\n" "$displaypath" >&2
    exit 1
  fi
'

printf 'Synchronizing submodule URLs...\n'
git -C "$repo_root" submodule sync --recursive

printf 'Updating submodules from their remote tracking branches...\n'
git -c maintenance.auto=false -C "$repo_root" \
  submodule update --init --recursive --remote

printf 'Updated submodules:\n'
git -C "$repo_root" submodule status --recursive
