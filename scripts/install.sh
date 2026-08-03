#!/usr/bin/env bash
# Install skills/ to ~/.codex/skills/ (Linux / macOS / WSL)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/skills"
DST="${HOME}/.codex/skills"

if [[ ! -d "${SRC}" ]]; then
  echo "[ERROR] skills folder not found: ${SRC}" >&2
  exit 1
fi

mkdir -p "${DST}"

MANAGED_STATE="${DST}/.bokujuu-cursorsetup-managed.txt"
LEGACY_MANAGED_NAMES=(
  # One-time migration for names managed before the ownership marker existed.
  "codex-session-doc"
  "empirical-prompt-tuning"
  "retrospective-codify"
  "skill-lifecycle"
  "system-structure-viz"
)

current_names=()
for skill_dir in "${SRC}"/*/; do
  [[ -d "${skill_dir}" ]] || continue
  current_names+=("$(basename "${skill_dir}")")
done

stale_names=()
if [[ -f "${MANAGED_STATE}" ]]; then
  while IFS= read -r name; do
    [[ "${name}" =~ ^[A-Za-z0-9_-]+$ ]] || continue
    if [[ ! -d "${SRC}/${name}" ]]; then
      stale_names+=("${name}")
    fi
  done < "${MANAGED_STATE}"
fi
for name in "${LEGACY_MANAGED_NAMES[@]}"; do
  if [[ ! -d "${SRC}/${name}" ]]; then
    stale_names+=("${name}")
  fi
done

for name in "${stale_names[@]}"; do
  [[ -n "${name}" ]] || continue
  target="${DST}/${name}"
  if [[ -d "${target}" ]]; then
    echo "[REMOVE] retired skill -> ${target}"
    rm -rf "${target}"
  fi
done

for skill_dir in "${SRC}"/*/; do
  [[ -d "${skill_dir}" ]] || continue
  name="$(basename "${skill_dir}")"
  target="${DST}/${name}"
  echo "[COPY] ${name} -> ${target}"
  rm -rf "${target}"
  cp -a "${skill_dir}" "${target}"
done

printf '%s\n' "${current_names[@]}" > "${MANAGED_STATE}"

find "${DST}" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "[OK] Global skills installed under ${DST}"
echo "[NEXT] Apply user-rules/ to Cursor Settings -> Rules -> User Rules (see docs/user-rules-guide.md)"
