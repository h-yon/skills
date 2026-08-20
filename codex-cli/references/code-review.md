# Code Review with Codex CLI

Distilled from openai/codex-plugin-cc (the official Codex plugin for Claude Code), reduced to plain CLI invocations so it works without the plugin's app-server runtime.

> Modified derivative work: this file rewrites the review workflow of [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (Apache License 2.0, Copyright 2026 OpenAI) as plain CLI invocations. See [../NOTICE](../NOTICE) and [../LICENSE](../LICENSE).

## Choosing the command

- `codex review` — built-in reviewer, human-readable report on stdout. No model/output flags.
- `codex exec review` — same reviewer with exec plumbing: `-m`, `-o <file>`, `--json`, `--output-schema`, `--ephemeral`. Prefer this when you need to capture or post-process the result.
- Neither accepts `-C`; run them from inside the target repository.
- Neither accepts `--sandbox`; the reviewer picks its own sandbox (observed on 0.147.0: `workspace-write [workdir, /tmp, $TMPDIR]`, so a review run is not read-only).
- Custom review instructions go in the positional `[PROMPT]` argument (or stdin via `-`). The plugin deliberately passes no custom text to the standard review and reserves focus text for the adversarial variant — mixing focus text into a standard review dilutes the built-in reviewer's own rubric.

## Target selection

Explicit targets:

| Target | Flag |
|--------|------|
| Staged + unstaged + untracked | `--uncommitted` |
| Branch diff against a base | `--base <ref>` (merge-base semantics, i.e. `<ref>...HEAD`) |
| Single commit | `--commit <sha>` |

Auto-selection logic (what the plugin does when the user doesn't specify):

1. If the working tree is dirty (any staged, unstaged, or untracked files) → `--uncommitted`.
2. Otherwise → `--base <default branch>`.

Detect the default branch in this order:

```bash
git symbolic-ref refs/remotes/origin/HEAD   # refs/remotes/origin/<name> → <name>
```

Fallback: try `main`, `master`, `trunk` as local heads, then as `origin/<name>`. If none exist, ask the user for `--base`.

Untracked files count as reviewable work even when `git diff --shortstat` is empty. Only conclude "nothing to review" when the relevant scope is actually empty; when in doubt, run the review.

## Size estimation: wait vs background

Estimate before running so the user isn't blocked on a long review:

```bash
git status --short --untracked-files=all
git diff --shortstat --cached && git diff --shortstat     # working-tree review
git diff --shortstat <base>...HEAD                        # branch review
```

- Clearly tiny (roughly 1–2 files, no directory-sized untracked additions) → run in the foreground.
- Anything larger or unclear → run as a background task (`run_in_background`) and report back when it finishes.

## Adversarial review

A distinct review mode that challenges the implementation approach, design choices, tradeoffs, and assumptions — not just a stricter pass over implementation defects. Run it as a plain `codex exec` with a purpose-built prompt and a JSON output contract:

```bash
SKILL_DIR=<absolute path of the directory holding this skill's SKILL.md>

codex exec --sandbox read-only --ephemeral \
  --output-schema "$SKILL_DIR/references/review-output.schema.json" \
  -o /tmp/adversarial-review.json \
  - < /tmp/adversarial-prompt.md
```

`--output-schema` needs a real path, so resolve `references/review-output.schema.json` against wherever this skill is installed instead of hard-coding a location.

Build `/tmp/adversarial-prompt.md` from [adversarial-review-prompt.md](adversarial-review-prompt.md) by filling the placeholders:

| Placeholder | Value |
|-------------|-------|
| `{{TARGET_LABEL}}` | e.g. `working tree diff` or `branch diff against origin/main` |
| `{{USER_FOCUS}}` | The user's focus text, or `No extra focus provided.` |
| `{{REVIEW_COLLECTION_GUIDANCE}}` | See below — inline vs self-collect |
| `{{REVIEW_INPUT}}` | The repository context (see below) |

### Context collection: inline vs self-collect

The plugin inlines the full diff only for small changes (≤ 2 files and ≤ 256 KB of diff); larger changes get a summary plus an instruction for Codex to collect the diff itself. Self-collect is usually the better default from the CLI — Codex reads the repo directly and the prompt stays small.

- Inline mode — `{{REVIEW_COLLECTION_GUIDANCE}}` = `Use the repository context below as primary evidence.` and `{{REVIEW_INPUT}}` contains the full diff:
  - working tree: `git status --short --untracked-files=all`, `git diff --cached --binary --no-ext-diff --submodule=diff`, `git diff --binary --no-ext-diff --submodule=diff`, plus untracked file bodies (skip binaries and files over ~24 KB)
  - branch: `git log --oneline --decorate <merge-base>..HEAD`, `git diff --stat <merge-base>..HEAD`, `git diff --binary --no-ext-diff --submodule=diff <merge-base>..HEAD`
- Self-collect mode — `{{REVIEW_COLLECTION_GUIDANCE}}` = `The repository context below is a lightweight summary. Inspect the target diff yourself with read-only git commands before finalizing findings.` and `{{REVIEW_INPUT}}` contains only status, shortstat, and the changed-file list.

### Output

The schema ([review-output.schema.json](review-output.schema.json)) enforces:

- `verdict`: `approve` | `needs-attention`
- `summary`: terse ship/no-ship assessment
- `findings[]`: `severity` (critical/high/medium/low), `title`, `body`, `file`, `line_start`, `line_end`, `confidence` (0–1), `recommendation`
- `next_steps[]`

The `-o` file contains the final JSON message. Parse failures happen; keep the raw output (`tee` the run) instead of re-running.

## Presenting review results

Rules the plugin enforces on the Claude side, worth keeping:

- Present findings first, ordered by severity, preserving the verdict / summary / findings / next-steps structure.
- Use file paths and line numbers exactly as Codex reports them.
- Preserve evidence boundaries: if Codex marked something as an inference or open question, keep that distinction.
- No findings → say so explicitly, with a brief residual-risk note.
- After presenting findings, STOP. Do not fix anything — ask the user which issues, if any, they want fixed before touching a single file, even when the fix is obvious.
- Malformed output or a failed run → show the most actionable stderr lines and stop; don't guess or substitute your own review.

## Follow-up

For adversarial reviews run via `codex exec` (without `--ephemeral` if you plan this), continue the same session:

```bash
codex exec resume --last "Explain finding #2 in more depth and propose a concrete patch"
```

Native `codex review` runs don't advertise a resume path; re-run with sharper instructions instead.
