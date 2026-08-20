# Advanced Codex CLI Usage

Verified against codex-cli 0.147.0. Flags churn between releases — on parse errors, check `codex exec --help` first.

## Removed / renamed flags

- `--full-auto` — removed. Use `--sandbox workspace-write` (exec runs never ask for approval anyway).
- Approval policy `-a/--ask-for-approval <untrusted|on-request|never>` exists only on the interactive `codex` command, not on `codex exec`.
- `--approve-for-me` (interactive) routes approval requests through automatic review with the workspace-write sandbox.

## Configuration Overrides

Use `-c key=value` for inline config overrides (dotted paths for nesting; value parsed as TOML):

```bash
codex exec -c model_reasoning_effort="high" "task"
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' "task"
codex exec -c shell_environment_policy.inherit=all "task"
```

Reasoning effort values: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`.

## Models

- `-m <model>` overrides; unset inherits `model` from `~/.codex/config.toml`.
- `*-spark` model variants (e.g. `gpt-5.3-codex-spark`) are the low-latency tier for quick tasks.

## Profiles

`-p <name>` layers `$CODEX_HOME/<name>.config.toml` on top of the base user config (profile-as-file, not a `[profiles]` section):

```bash
codex exec -p review "Review this code"    # loads ~/.codex/review.config.toml
```

## Structured / machine-readable output

```bash
codex exec --output-schema schema.json -o /tmp/result.json "Analyze and return structured results"
codex exec --json "task" 2>/dev/null | jq .    # JSONL event stream
```

## Session Management

```bash
codex exec resume --last "follow-up prompt"   # continue the last exec session
codex resume --last                           # interactive: continue most recent
codex fork --last                             # interactive: fork most recent
codex apply                                   # git-apply the latest diff produced by the agent
```

`--ephemeral` skips session persistence entirely (no resume possible).

## Isolation and repo checks

| Flag | Effect |
|------|--------|
| `--skip-git-repo-check` | Allow running outside a Git repository |
| `--ignore-user-config` | Don't load `~/.codex/config.toml` (auth still works) |
| `--ignore-rules` | Don't load execpolicy `.rules` files |
| `--add-dir <dir>` | Extra writable directories alongside the workspace |

## Web search

`--search` enables the native `web_search` tool for the run (no per-call approval).

## Local/OSS Models

```bash
codex exec --oss --local-provider ollama "task"    # or lmstudio
```

## Feature Flags

```bash
codex features list                     # inspect available flags and their stability
codex exec --enable <feature> --disable <feature> "task"
```

## Diagnostics

```bash
codex doctor    # check installation, config, auth, runtime health
```
