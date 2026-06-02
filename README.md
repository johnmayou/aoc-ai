# aoc-ai

My solutions to [Advent of Code 2025](https://adventofcode.com/2025), used as a live experiment in AI-assisted development.

<details>
    <summary>What is Advent of Code?</summary>
    [Advent of Code](https://adventofcode.com/2025) is an annual series of small programming puzzles released daily through December. Each day unlocks two parts; Part 2 is hidden until you solve Part 1. The puzzles are self-contained and well-specified, which makes them a good testbed for an AI-driven workflow: clear inputs, known sample answers, and a single correct output to verify against.
</details>

## Why this repo exists

A recruiter asked: _"How do you use AI in your workflow?"_

I didn't have a great answer.

So I set out to figure that out. This repo is a testing ground for evaluating AI development tools and practices, using Advent of Code puzzles as the vehicle to put them into use. There's a lot to learn, and the answers keep changing as I go.

## The tool stack

**[Claude Code](https://claude.ai/code)** — the AI coding assistant doing the implementation work. It reads puzzle descriptions, writes failing tests, implements solutions, runs them, and reports answers.

**[superpowers-beads](https://github.com/jbongaarts/superpowers-beads)** — a plugin for Claude Code that installs discipline as skills: test-driven development, systematic debugging, verification before completion, code review, and more. Instead of the AI defaulting to "write code and hope," these skills enforce a specific process: RED/GREEN/REFACTOR, root-cause before fix, never close a task without verified output.

**[bd (beads)](https://github.com/gastownhall/beads)** — a local issue tracker that persists across AI sessions. Because each conversation starts fresh, bd is how the agent knows what's been done, what's in progress, and what's next. It's the memory layer.

## The workflow

Every puzzle day follows the same loop:

1. I paste the puzzle instructions into `prompt/day_NN.txt` and my personal input into `input/day_NN.txt`
2. I tell the agent which day and part to solve: _"Solve Day 1 Part 1"_
3. The agent reads the prompt (which includes a sample test case), writes a **failing test** first, confirms it fails for the right reason, then implements the solution until the test is green
4. It runs the solution against my real input and reports the answer
5. I submit on the AoC site and confirm; only then does the agent close the bd issue
6. The agent commits the solution and pushes to remote

## Progress

| Day | Part 1 | Part 2 |
| --- | ------ | ------ |
| 01  | ✓      | ✓      |
| 02  | ✓      | ✓      |
| 03  | ✓      | ✓      |
| 04  | ✓      | ✓      |
| 05  | ✓      | ✓      |
| 06  | ✓      | ✓      |
| 07  | ✓      | ✓      |
| 08  | ✓      | ✓      |
| 09  | ✓      | ✓      |
| 10  | ✓      | ✓      |
| 11  | ✓      | ✓      |
| 12  |        |        |

## What's next

The tool stack feels solid for what I'm trying to do, that part is working.

The natural next question is scale: what happens when one agent isn't enough? I'm looking into multi-agent orchestration next:

- [Hive](https://github.com/colonyops/hive) — surfaced at a recent [GoMN meetup talk](https://www.meetup.com/golangmn/events/314701730) on how Grafana uses AI in their actual development workflow
- [gastown](https://github.com/gastownhall/gastown) — multi-agent orchestration from the same team behind beads
- [Claude's dynamic workflows](https://code.claude.com/docs/en/workflows) — Claude's answer to multi-agent orchestration, currently in research preview

So, back to the original question: _"How do you use AI in your workflow?"_, I'm still figuring that out, but this is a step in the right direction 🙂

## License

[MIT](LICENSE)
