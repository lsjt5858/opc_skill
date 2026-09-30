#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="$repo_root/scripts/update-submodules.sh"
tmp_dirs=()

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

cleanup() {
  local path

  for path in "${tmp_dirs[@]}"; do
    rm -rf "$path"
  done
}

trap cleanup EXIT

configure_repository() {
  local repository="$1"

  git -C "$repository" config user.name "Submodule Test"
  git -C "$repository" config user.email "submodule-test@example.com"
  git -C "$repository" config core.hooksPath /dev/null
}

test_dry_run_does_not_change_repository() {
  local before after output

  before="$(git -C "$repo_root" status --porcelain=v1)"
  output="$(bash "$script_path")"
  after="$(git -C "$repo_root" status --porcelain=v1)"

  [[ "$output" == *"[dry-run]"* ]] || fail "dry-run marker is missing"
  [[ "$output" == *"--execute"* ]] || fail "execute hint is missing"
  [[ "$before" == "$after" ]] || fail "dry-run changed the repository"
}

test_execute_updates_to_remote_head() {
  local fixture child_remote child_source parent trace latest actual

  fixture="$(mktemp -d)"
  tmp_dirs+=("$fixture")
  child_remote="$fixture/child.git"
  child_source="$fixture/child-source"
  parent="$fixture/parent"
  trace="$fixture/git-trace.json"

  git -c init.defaultBranch=main init --bare "$child_remote" >/dev/null
  git --git-dir="$child_remote" symbolic-ref HEAD refs/heads/main

  git -c init.defaultBranch=main init "$child_source" >/dev/null
  configure_repository "$child_source"
  printf 'v1\n' >"$child_source/version.txt"
  git -C "$child_source" add version.txt
  git -C "$child_source" commit -m "initial version" >/dev/null
  git -C "$child_source" remote add origin "$child_remote"
  git -C "$child_source" push -u origin main >/dev/null

  git -c init.defaultBranch=main init "$parent" >/dev/null
  configure_repository "$parent"
  mkdir -p "$parent/scripts"
  cp "$script_path" "$parent/scripts/update-submodules.sh"
  GIT_ALLOW_PROTOCOL=file git -C "$parent" submodule add "$child_remote" deps/child >/dev/null
  git -C "$parent" add .
  git -C "$parent" commit -m "add child submodule" >/dev/null

  printf 'v2\n' >"$child_source/version.txt"
  git -C "$child_source" add version.txt
  git -C "$child_source" commit -m "latest version" >/dev/null
  git -C "$child_source" push origin main >/dev/null
  latest="$(git -C "$child_source" rev-parse HEAD)"

  GIT_ALLOW_PROTOCOL=file GIT_TRACE2_EVENT="$trace" \
    bash "$parent/scripts/update-submodules.sh" --execute >/dev/null
  actual="$(git -C "$parent/deps/child" rev-parse HEAD)"

  [[ "$actual" == "$latest" ]] || fail "--execute did not update to remote HEAD"
  if rg -q '"argv":.*"maintenance","run","--auto"' "$trace"; then
    fail "--execute started automatic Git maintenance"
  fi
}

test_execute_rejects_dirty_submodule() {
  local fixture child_remote child_source parent output

  fixture="$(mktemp -d)"
  tmp_dirs+=("$fixture")
  child_remote="$fixture/child.git"
  child_source="$fixture/child-source"
  parent="$fixture/parent"

  git -c init.defaultBranch=main init --bare "$child_remote" >/dev/null
  git --git-dir="$child_remote" symbolic-ref HEAD refs/heads/main

  git -c init.defaultBranch=main init "$child_source" >/dev/null
  configure_repository "$child_source"
  printf 'tracked\n' >"$child_source/version.txt"
  git -C "$child_source" add version.txt
  git -C "$child_source" commit -m "initial version" >/dev/null
  git -C "$child_source" remote add origin "$child_remote"
  git -C "$child_source" push -u origin main >/dev/null

  git -c init.defaultBranch=main init "$parent" >/dev/null
  configure_repository "$parent"
  mkdir -p "$parent/scripts"
  cp "$script_path" "$parent/scripts/update-submodules.sh"
  GIT_ALLOW_PROTOCOL=file git -C "$parent" submodule add "$child_remote" deps/child >/dev/null
  printf 'local change\n' >>"$parent/deps/child/version.txt"

  if output="$(GIT_ALLOW_PROTOCOL=file bash "$parent/scripts/update-submodules.sh" --execute 2>&1)"; then
    fail "--execute accepted a dirty submodule"
  fi

  [[ "$output" == *"Refusing to update dirty submodule: deps/child"* ]] ||
    fail "dirty submodule error is missing"
}

test_dry_run_does_not_change_repository
test_execute_updates_to_remote_head
test_execute_rejects_dirty_submodule
printf 'PASS: update-submodules dry-run\n'
printf 'PASS: update-submodules execute\n'
printf 'PASS: update-submodules dirty protection\n'
