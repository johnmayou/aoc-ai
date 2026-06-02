# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->

## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->

## Git Commits

**Always commit `.beads/interactions.jsonl` and `.beads/issues.jsonl` if modified.** After `bd close` or any beads operation, run `git status` before pushing — beads files are often modified and must be staged and committed in a separate commit before `git pull --rebase`.

**`cat` is aliased to `kat` (a `bat` wrapper) in this environment.** `bat` does not accept heredoc stdin, so the system default of `$(cat <<'EOF'...EOF)` for commit messages silently returns an empty string and aborts the commit.

**Always use `\cat` to bypass the alias:**

```bash
git commit -m "$(\cat <<'EOF'
feat: subject line

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

The leading `\` forces the real `/bin/cat`, bypassing the alias.

## Build & Test

| Command      | Description      |
| ------------ | ---------------- |
| `make fmt`   | Format Python    |
| `make lint`  | Lint Python      |
| `make flint` | Format then lint |
| `make test`  | Run all tests    |

## Architecture Overview

```
src/day_NN_P.py       # solution — N = day number, P = part (1 or 2)
prompt/day_NN.txt     # puzzle instructions — part 1 at top, part 2 below "--- Part Two ---"
input/day_NN.txt      # personal puzzle input (gitignored)
```

`day_NN` is consistent across all three: `src/day_02_1.py` reads from `input/day_02.txt` and its puzzle is in `prompt/day_02.txt`.

**All `src/day_NN_P.py` files are pre-created as empty stubs in the repository.** Before writing any solution file, always `Read` it first — even if you expect it to be empty or new. The `Write` tool will fail if you skip this step for an existing file.

## When a Command Fails Unexpectedly

If a command fails that you expected to succeed:

1. **Stop** — do not work around it or retry blindly.
2. **Root cause it** — read the error carefully, check tool docs, inspect file state, check what assumptions you made that might be wrong.
3. **Update instructions** — once you understand why, add a note to the relevant CLAUDE.md (or `bd remember`) so it cannot recur.
4. **If you cannot determine the cause** — ask the user for help before proceeding. Do not guess and move on.

## Definition of Done

For tasks where the **primary objective is to solve the puzzle**, the issue is **not complete** until all of the following are true:

1. `make flint` passes (format + lint, zero errors)
2. `make test` passes (all tests green)
3. **Answer verified on AoC website** — YOU run `python src/day_NN_P.py` against the real `input/day_NN.txt`, report the output to the user, and wait for them to confirm it was accepted on the AoC website.

Never close a puzzle-solving issue or claim the work is done without explicit user confirmation that step 3 was accepted.

For other tasks (refactoring, docstrings, tooling, etc.), steps 1 and 2 are sufficient.

## Python Execution

**Never use `python -c "..."` to run arbitrary Python.** Use only:
- `python src/day_NN_P.py` — to run the solution against real input
- `pytest` / `make test` — to run tests

## Conventions & Patterns

- Tests live in the same file as the solution — write `test_*` functions directly in `day_NN_P.py`. No separate test file needed. pytest discovers tests in all `*.py` files via `python_files = ["*.py"]` in `pyproject.toml`.
- Never read the full contents of `input/day_NN.txt` — these files can be large. Read only the first few lines to understand the format.
- Docstrings: be pragmatic — only add one when the WHY or the mental model is non-obvious. Use the multi-line format always:
  ```python
  """
  docstring here
  """
  ```
  Never use the inline form `"""docstring here"""`.
- Each solution file follows this three-function structure:
  - `parse(data: str) -> <T>` — converts raw input string into a structured data type
  - `solve(parsed: <T>) -> <answer>` — pure logic, no IO; takes parsed data and returns the answer
  - `main()` — reads `input/day_NN.txt`, calls `parse()` then `solve()`, and prints the result
  - Run with `python src/day_NN_P.py`
  - Tests call `solve(parse(SAMPLE))` to exercise both layers together
