# Advanced Codex CLI Usage

Verified against codex-cli 0.160.1. Flags churn between releases — on parse errors, check `codex exec --help` first.

## Removed / renamed flags

- `--full-auto` — removed. Use `--sandbox workspace-write` (exec runs never ask for approval anyway).
- Approval policy `-a/--ask-for-approval <on-request|never>` exists only on the interactive `codex` command, not on `codex exec` (`untrusted` is no longer a listed value as of 0.160.1).
- `--approve-for-me` (interactive and `codex exec`) routes approval requests through automatic review with the workspace-write sandbox.

## Configuration Overrides

Use `-c key=value` for inline config overrides (dotted paths for nesting; value parsed as TOML):

```bash
codex exec -c model_reasoning_effort="high" "task" < /dev/null
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' "task" < /dev/null
codex exec -c shell_environment_policy.inherit=all "task" < /dev/null
```

Reasoning effort values depend on the model: `low`, `medium`, `high`, `xhigh` are common, and some models add `max` and `ultra`. Check per-model support in the catalog (below).

## Models

- `-m <model>` overrides; unset inherits `model` from `~/.codex/config.toml`.
- `codex debug models` prints the model catalog as JSON, including each model's supported reasoning levels.

## Profiles

`-p <name>` layers `$CODEX_HOME/<name>.config.toml` on top of the base user config (profile-as-file, not a `[profiles]` section):

```bash
codex exec -p review "Review this code" < /dev/null    # loads ~/.codex/review.config.toml
```

## Structured / machine-readable output

```bash
codex exec --output-schema schema.json -o /tmp/result.json "Analyze and return structured results" < /dev/null
codex exec --json "task" < /dev/null 2>/dev/null | jq .    # JSONL event stream
```

## Session Management

```bash
codex exec resume --last "follow-up prompt"   # continue the last exec session
codex resume --last                           # interactive: continue most recent interactive session
codex fork --last                             # interactive: fork most recent
codex apply <TASK_ID>                         # git-apply the diff of a Codex Cloud task
```

`codex resume --last` skips exec sessions unless `--include-non-interactive` is given.

`--ephemeral` skips session persistence entirely (no resume possible).

## Isolation and repo checks

| Flag | Effect |
|------|--------|
| `--skip-git-repo-check` | Allow running outside a Git repository |
| `--ignore-user-config` | Don't load `~/.codex/config.toml` (auth still works) |
| `--ignore-rules` | Don't load execpolicy `.rules` files |
| `--add-dir <dir>` | Extra writable directories alongside the workspace |

## Web search

`--search` enables the native `web_search` tool for the run (no per-call approval). It is a top-level flag: `codex exec --search` is rejected, so put it before the subcommand.

```bash
codex --search exec --sandbox read-only -C <dir> "task" < /dev/null
```

## Local/OSS Models

```bash
codex exec --oss --local-provider ollama "task" < /dev/null    # or lmstudio
```

## Feature Flags

```bash
codex features list                     # inspect available flags and their stability
codex exec --enable <feature> --disable <feature> "task" < /dev/null
```

## Diagnostics

```bash
codex doctor    # check installation, config, auth, runtime health
```
