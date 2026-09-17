# The Perfection System

An agent-neutral skill for improving an artifact through bounded revision, separate review passes, and evidence-based acceptance.

Use it for writing, code, research, prompts, plans, and design specifications. Run it with one assistant, multiple reviewers, or a human coordinating the work. The core requires only the ability to read instructions and produce an artifact. It does not require a particular model, provider, orchestration framework, shell, network connection, or persistent memory.

"Perfection" names the project. It does not promise flawless output or make reviewer agreement a substitute for evidence.

## Start here

**Any chat or instruction-based environment:** supply `THE-PERFECTION-SYSTEM.md`, your artifact, and your objective. That file is a complete standalone copy of the core instructions. Upload it, paste its contents, or have your environment read it. Merely linking a file does not ensure its contents were loaded.

**An environment that supports Agent Skills:** copy the entire `skills/the-perfection-system/` directory into a skill location that your host actually supports. Keep the directory name `the-perfection-system`. The package uses the standard `SKILL.md` layout and required metadata [1]. Discovery paths, activation syntax, and tool permissions remain host-specific [2].

**An API or custom harness:** supply the Markdown body of `SKILL.md` through your application's supported instruction mechanism, subordinate to its existing instruction hierarchy. Map the workflow's capabilities to actual tools only when they are available and authorized. A plain prompt is sufficient for single-assistant mode.

Example request after loading the skill:

```text
Use The Perfection System to improve the attached onboarding guide.
Preserve all product claims, prices, and policy requirements.
Audience: a first-time customer. Output: the revised guide.
Required checks: preserve meaning, remove contradictions, make each action clear.
Use at most three review cycles. Report any checks you cannot verify.
```

For code, add the editable files, expected behavior, and relevant checks. For research, add the question, source expectations, and date sensitivity. For a short wording edit, one revision and review pass is enough.

## What the workflow does

1. Establishes the objective, authority, immutable constraints, observable criteria, and a finite budget.
2. Lets one editor revise while separate critique and continuity lenses diagnose a frozen candidate.
3. Checks evidence, disagreements, and regressions against the same candidate and contract.
4. Stops with `accepted`, `blocked`, `budget_exhausted`, `stalled`, or `stopped`, and delivers the artifact with appropriate limitations.

The default budget is three review cycles, not three mandatory rewrites. A valid first candidate may pass immediately. Required criteria must all pass; advisory suggestions do not force endless polishing.

## Portability contract

| Available environment | Behavior |
| --- | --- |
| Plain chat, no tools | Keep the artifact and compact state in the conversation; label external or executable checks unverified. |
| One assistant with tools | Alternate edit and review passes; use only tools actually provided and authorized. |
| Multiple reviewers | Freeze one integrated candidate; require same-cycle, same-version approval from every required lens. |
| Human coordination | Transfer explicit artifacts and records; do not assume automated orchestration. |
| New session or different harness | Load the checkpoint and actual source material; revalidate versions and remaining budget. |

The skill is designed to be portable at the instruction level. It cannot make every host discover skills, add missing capabilities, guarantee instruction-following quality, or turn a single model's self-review into independent validation. No live cross-host or cross-model compatibility benchmark is claimed.

The repository's historical name does not impose a runtime dependency. No vendor configuration, model identifier, slash command, agent-launch API, or special memory feature is required.

## Files

| Path | Purpose |
| --- | --- |
| `skills/the-perfection-system/SKILL.md` | Canonical, self-contained skill instructions. Edit this first. |
| `THE-PERFECTION-SYSTEM.md` | Generated standalone edition, preserving the original entry point. |
| `skills/the-perfection-system/references/` | Optional review detail and worked examples. |
| `skills/the-perfection-system/assets/run-template.md` | Optional contract, review, and handoff template. |
| `tests/scenarios.json` | Behavioral evaluation cases for a human or external harness. |
| `scripts/validate.py` | Offline repository checks and standalone-copy generation. |
| `tests/test_validate.py` | Automated tests of the repository validator. |
| `CHANGELOG.md` | Changes from the original architecture. |

No install command or code execution is needed to use the skill. Python 3.9 or later is needed only for the optional maintainer checks; they use the standard library and make no network requests.

## Maintain and validate

From the repository root:

```sh
python3 scripts/validate.py --sync
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

`--sync` regenerates only `THE-PERFECTION-SYSTEM.md` from the canonical skill. The validator checks the package's deliberately small frontmatter format, required files, relative Markdown link targets, standalone consistency, and behavioral-case structure. It is not a general YAML parser, a model evaluator, or a proof of semantic correctness.

Run the behavioral cases in `tests/scenarios.json` separately with the actual model and environment being evaluated. Record the skill revision, model or participant, available capabilities, output, and whether every expected behavior occurred. Do not report these scenarios as passed merely because the JSON validates. The worked examples are illustrative, not execution logs.

Before publishing a change, review whether it introduces a vendor-specific dependency, weakens a required acceptance gate, or allows unverifiable claims. Do not commit real user artifacts, secrets, or private checkpoint records as examples.

## Design references

Only the packaging and integration conventions are attributed to these references. The refinement protocol and its default budgets are project design choices, not externally proven performance claims. Sources checked September 17, 2026.

[1] Agent Skills. "Specification." Official documentation.
https://agentskills.io/specification

[2] Agent Skills. "How to add skills support to your agent." Official documentation.
https://agentskills.io/client-implementation/adding-skills-support
