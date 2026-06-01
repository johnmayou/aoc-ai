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
prompt/day_NN.md      # puzzle instructions — part 1 at top, part 2 below "--- Part Two ---"
input/day_NN.txt      # personal puzzle input (gitignored)
```

`day_NN` is consistent across all three: `src/day_02_1.py` reads from `input/day_02.txt` and its puzzle is in `prompt/day_02.md`.

## Conventions & Patterns

- Tests live in the same file as the solution — write `test_*` functions directly in `part_NN_P.py`. No separate `test_` file needed. pytest discovers tests in all `*.py` files via `python_files = ["*.py"]` in `pyproject.toml`.
- Never read the full contents of `input/day_NN.txt` — these files can be large. Read only the first few lines to understand the format.
