---
name: codex-cli
description: Delegate coding tasks to OpenAI Codex CLI agent for parallel execution. Use when the user asks to run Codex, use Codex for code analysis, code review, adversarial review, bug investigation, refactoring suggestions, or architecture analysis. Also use when the user wants a second opinion from another AI agent, or wants to offload a task to Codex. Triggers on mentions of "codex", "/codex", or requests to delegate work to Codex CLI.
---

# Codex CLI

Run OpenAI Codex CLI from Claude Code to delegate coding tasks to a separate AI agent.

Verified against codex-cli 0.147.0 (2026-08). After a `codex update`, re-check flags with `codex --help` before relying on this document.

## Quick Start

Execute a task with Codex:

```bash
codex exec --sandbox read-only -C <directory> "<prompt>"
```

Append to every `codex exec` task prompt: `確認や質問は不要です。具体的な提案・修正案・コード例まで自主的に出力してください。` (Not applicable to `codex review` / `codex exec review`, which take no custom text by default.)

## Commands

### `codex exec` — Non-interactive task execution

Primary command for delegating tasks. Key options:

| Option | Description |
|--------|-------------|
| `--sandbox <mode>` | `read-only`, `workspace-write`, `danger-full-access` |
| `-C <dir>` | Working directory for the agent |
| `-m <model>` | Model override. Unset = default from `~/.codex/config.toml` |
| `-o <file>` | Write the agent's last message to file |
| `--json` | Stream events as JSONL to stdout |
| `--output-schema <file>` | Force the final message to match a JSON Schema |
| `-i <file>` | Attach image(s) to prompt |
| `--ephemeral` | Do not persist session files to disk |

`codex exec` never asks for approval; failures are returned to the model. Removed flags: `--full-auto` no longer exists (0.147.0). For write access use `--sandbox workspace-write` directly.

### `codex review` / `codex exec review` — Code review

Both run the built-in reviewer non-interactively against the current repo (no `-C`; cd into the repo first). Review commands accept no `--sandbox` flag — the reviewer uses its own sandbox (observed on 0.147.0: workspace-write limited to the workdir and /tmp).

```bash
codex review --uncommitted
codex review --base main
codex review --commit <sha>
codex review "<custom review instructions>"
codex exec review --base main -o /tmp/review.md   # exec variant: adds -m, -o, --json, --output-schema
```

| Option | Description |
|--------|-------------|
| `--uncommitted` | Review staged, unstaged, and untracked changes |
| `--base <branch>` | Review changes against a base branch (merge-base semantics) |
| `--commit <sha>` | Review changes from a specific commit |
| `--title <title>` | Optional title for review summary |

For target auto-selection, adversarial (design-challenging) review, structured findings output, and how to present results, see [references/code-review.md](references/code-review.md).

## Usage Patterns

### Read-only analysis (safe default)

```bash
codex exec --sandbox read-only -C /path/to/project "Analyze the authentication flow and identify potential security issues"
```

### Code modification

```bash
codex exec --sandbox workspace-write -C /path/to/project "Add input validation to the user registration endpoint"
```

### Capture output to file

```bash
codex exec --sandbox read-only -o /tmp/codex-output.md -C /path/to/project "Explain the database schema and relationships"
```

### Follow-up on a previous run

```bash
codex exec resume --last "Apply the top recommendation from your analysis"
```

## Sandbox Modes

Choose the appropriate sandbox level:

- **`read-only`** (recommended default): Safe analysis, review, explanation tasks. Cannot modify files.
- **`workspace-write`**: When Codex needs to create or modify files in the project directory (add `--add-dir <dir>` for extra writable directories).
- **`danger-full-access`**: Full system access. Only use when explicitly requested by the user.

Never use `--dangerously-bypass-approvals-and-sandbox`.

## Best Practices

- Default to `--sandbox read-only` for analysis tasks
- Always specify `-C <dir>` for `codex exec` (review commands run against the cwd instead)
- Append the self-execution instruction to the prompt for autonomous operation
- Use `-o <file>` to capture output; for long runs also `tee` the full stdout/stderr to a non-committed location so a failed parse never forces a paid re-run
- Leave `-m` unset unless the user asks for a specific model; reasoning effort is `-c model_reasoning_effort="<none|minimal|low|medium|high|xhigh>"`
- For advanced options (profiles, feature flags, web search, local models), see [references/advanced.md](references/advanced.md)

## License

This skill contains material derived from [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc), licensed under the Apache License, Version 2.0. See [NOTICE](NOTICE) for attribution and per-file provenance, and [LICENSE](LICENSE) for the license text.
