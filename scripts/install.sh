#!/usr/bin/env bash
# Install skills/ to ~/.codex/skills/ (Linux / macOS / WSL)
set -euo pipefail

install_codex_mcp=false
sync_args=()
codex_filesystem_root=""

while (($# > 0)); do
  case "$1" in
    --dry-run)
      sync_args+=(--dry-run)
      shift
      ;;
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
      echo "Usage: ./scripts/install.sh [--dry-run] [--install-codex-mcp] [--codex-filesystem-root PATH]"
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "${ROOT}/scripts/sync_skills.py" "${sync_args[@]}"
if [[ " ${sync_args[*]} " == *" --dry-run "* ]]; then
  exit 0
fi

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

  uvx_cmd="$(command -v uvx 2>/dev/null || true)"
  if [[ -z "${uvx_cmd}" && -x "${HOME}/.local/bin/uvx" ]]; then
    uvx_cmd="${HOME}/.local/bin/uvx"
  fi
  if [[ -z "${uvx_cmd}" ]]; then
    uvx_cmd="uvx"
  fi
  if codex mcp get blender --json >/dev/null 2>&1; then
    echo "[SKIP] Codex MCP already exists: blender"
  else
    echo "[ADD] Codex MCP blender -> ${uvx_cmd} --python 3.11 blender-mcp"
    codex mcp add blender \
      --env UV_PYTHON_PREFERENCE=only-managed \
      --env DISABLE_TELEMETRY=true \
      --env BLENDER_HOST=localhost \
      --env BLENDER_PORT=9876 \
      -- "${uvx_cmd}" --python 3.11 blender-mcp
  fi
  echo "[OK] Codex MCP registered in the user-wide Codex configuration (run 'codex mcp list' to verify)"
fi
