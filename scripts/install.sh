#!/usr/bin/env bash
# Install skills/ to ~/.codex/skills/ (Linux / macOS / WSL)
set -euo pipefail

install_codex_mcp=false
codex_filesystem_root=""

while (($# > 0)); do
  case "$1" in
    --install-codex-mcp)
      install_codex_mcp=true
      shift
      ;;
    --codex-filesystem-root)
      if (($# < 2)); then
        echo "[ERROR] --codex-filesystem-root requires a directory" >&2
        exit 2
      fi
      codex_filesystem_root="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: ./scripts/install.sh [--install-codex-mcp] [--codex-filesystem-root PATH]"
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

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
else
  for name in "${LEGACY_MANAGED_NAMES[@]}"; do
    if [[ ! -d "${SRC}/${name}" ]]; then
      stale_names+=("${name}")
    fi
  done
fi

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

codex_mcp_add_if_missing() {
  local name="$1"
  shift
  if codex mcp get "${name}" --json >/dev/null 2>&1; then
    echo "[SKIP] Codex MCP already exists: ${name}"
    return
  fi
  echo "[ADD] Codex MCP ${name} -> $*"
  codex mcp add "${name}" -- "$@"
}

if [[ "${install_codex_mcp}" == true ]]; then
  if ! command -v codex >/dev/null 2>&1; then
    echo "[ERROR] codex command not found. Add Codex CLI to PATH before using --install-codex-mcp." >&2
    exit 1
  fi

  if [[ -n "${codex_filesystem_root}" ]]; then
    if [[ ! -d "${codex_filesystem_root}" ]]; then
      echo "[ERROR] Codex filesystem root is not a directory: ${codex_filesystem_root}" >&2
      exit 1
    fi
    codex_filesystem_root="$(cd "${codex_filesystem_root}" && pwd)"
    codex_mcp_add_if_missing "filesystem" npx -y @modelcontextprotocol/server-filesystem "${codex_filesystem_root}"
  else
    echo "[SKIP] Codex MCP filesystem (pass --codex-filesystem-root to enable)"
  fi

  codex_mcp_add_if_missing "memory" npx -y @modelcontextprotocol/server-memory
  codex_mcp_add_if_missing "codex-sol" codex mcp-server -c 'model="gpt-5.6-sol"'
  codex_mcp_add_if_missing "codex-terra" codex mcp-server -c 'model="gpt-5.6-terra"'
  codex_mcp_add_if_missing "codex-luna" codex mcp-server -c 'model="gpt-5.6-luna"'
  echo "[OK] Codex MCP registered in the user-wide Codex configuration (run 'codex mcp list' to verify)"
fi
