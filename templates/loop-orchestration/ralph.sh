#!/usr/bin/env bash
# Outer Ralph loop for Linux / WSL (Tier 4 — workaround D).
# Prereqs: cursor-agent on PATH, CURSOR_API_KEY set, PROMPT.md present.
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${1:-$(pwd)}"
MAX_ITERATIONS="${MAX_ITERATIONS:-3}"
STOP_ON_COMPLETE="${STOP_ON_COMPLETE:-0}"
MODEL="${MODEL:-composer-2.5}"
PROMPT_FILE="${KIT_DIR}/PROMPT.md"
JOURNAL="${KIT_DIR}/loop-journal.txt"
ITERATION_FILE="${KIT_DIR}/current-iteration.txt"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "PROMPT.md not found (copy PROMPT.md.template)" >&2
  exit 1
fi

ts() { date '+%Y/%m/%d %H:%M'; }

get_promise() {
  if grep -q '<promise>COMPLETE</promise>' <<<"$1"; then echo COMPLETE; return; fi
  if grep -q '<promise>ITERATION_DONE</promise>' <<<"$1"; then echo ITERATION_DONE; return; fi
  echo UNKNOWN
}

cd "$WORKSPACE"
for ((i = 1; i <= MAX_ITERATIONS; i++)); do
  echo "$i" >"$ITERATION_FILE"
  echo "$(ts) | 反復 ${i}/${MAX_ITERATIONS} 開始（オーケストレータ）" >>"$JOURNAL"

  output="$(cursor-agent -p --workspace "$WORKSPACE" --output-format text --model "$MODEL" "$(cat "$PROMPT_FILE")" 2>&1)" || true
  printf '%s\n' "$output"

  promise="$(get_promise "$output")"
  echo "$(ts) | 反復 ${i}/${MAX_ITERATIONS} 終了 | agent: ${promise}" >>"$JOURNAL"

  if [[ "$STOP_ON_COMPLETE" == "1" && "$promise" == "COMPLETE" ]]; then
    break
  fi
done
