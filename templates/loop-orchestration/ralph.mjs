/**
 * Ralph outer loop via @cursor/sdk TypeScript (Tier 2 — workaround F).
 *
 * Prereqs: npm install @cursor/sdk, CURSOR_API_KEY set, PROMPT.md in kit dir.
 *
 * Usage (from target repo root):
 *   node path/to/ralph.mjs
 *   MAX_ITERATIONS=5 STOP_ON_COMPLETE=1 node path/to/ralph.mjs
 */
import { readFileSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { Agent } from "@cursor/sdk";

const kitDir = dirname(fileURLToPath(import.meta.url));
const workspace = process.cwd();
const maxIterations = Number(process.env.MAX_ITERATIONS ?? "3");
const stopOnComplete = process.env.STOP_ON_COMPLETE === "1";
// Default: composer-2.5 (loop cost). Override for Grok, e.g. CURSOR_MODEL=grok-4.5-xhigh
const modelId = process.env.CURSOR_MODEL ?? "composer-2.5";
const promptPath = join(kitDir, "PROMPT.md");
const journal = join(kitDir, "loop-journal.txt");
const iterationFile = join(kitDir, "current-iteration.txt");

const apiKey = process.env.CURSOR_API_KEY;
if (!apiKey) {
  console.error("CURSOR_API_KEY unset");
  process.exit(2);
}
if (!existsSync(promptPath)) {
  console.error("PROMPT.md not found — copy PROMPT.md.template");
  process.exit(2);
}

const prompt = readFileSync(promptPath, "utf8");
const ts = () =>
  new Date()
    .toLocaleString("sv-SE", { timeZone: "Asia/Tokyo" })
    .replace("T", " ")
    .slice(0, 16);

function journalLine(line) {
  appendFileSync(journal, `${ts()} | ${line}\n`, "utf8");
}

function getPromise(text) {
  if (text.includes("<promise>COMPLETE</promise>")) return "COMPLETE";
  if (text.includes("<promise>ITERATION_DONE</promise>")) return "ITERATION_DONE";
  return "UNKNOWN";
}

const agent = await Agent.create({
  apiKey,
  model: { id: modelId },
  local: { cwd: workspace },
});

try {
  for (let i = 1; i <= maxIterations; i++) {
    writeFileSync(iterationFile, String(i), "utf8");
    journalLine(`反復 ${i}/${maxIterations} 開始（SDK orchestrator）`);

    const run = await agent.send(prompt);
    const result = await run.wait();
    const text = result.result ?? "";
    console.log(text);
    const promise = getPromise(text);
    journalLine(`反復 ${i}/${maxIterations} 終了 | agent: ${promise}`);

    if (stopOnComplete && promise === "COMPLETE") break;
  }
} finally {
  if (typeof agent.dispose === "function") await agent.dispose();
}
