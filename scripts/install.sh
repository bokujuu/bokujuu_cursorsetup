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

for skill_dir in "${SRC}"/*/; do
  name="$(basename "${skill_dir}")"
  target="${DST}/${name}"
  echo "[COPY] ${name} -> ${target}"
  rm -rf "${target}"
  cp -a "${skill_dir}" "${target}"
done

find "${DST}" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "[OK] Global skills installed under ${DST}"
echo "[NEXT] Apply user-rules/ to Cursor Settings -> Rules -> User Rules (see docs/user-rules-guide.md)"
