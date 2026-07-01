---
name: docs-sync-guardian
description: Keep repository documentation aligned with code, configuration, asset, API, release, workflow, or product changes. Use whenever Codex modifies a repo that has docs-as-contract expectations, when a user says docs must stay in sync, before finalizing a feature/fix, or when reviewing a diff for stale README, roadmap, specs, changelog, agent instructions, or handoff notes.
---

# Docs Sync Guardian

## Overview

Treat docs as part of the change, not an afterthought. The goal is to leave future agents and humans with a truthful map of what changed, what did not change, and what remains intentionally out of scope.

## Core Rule

After code changes, documentation is suspicious until checked against the current implementation. Be aggressive when searching for drift and conservative when editing.

Use this trust order:

1. Working implementation, generated artifacts, and current runtime behavior.
2. Public API, schema, CLI, configuration, exported types, and examples that compile or run.
3. Tests, fixtures, migrations, and release artifacts.
4. Documentation.

When docs and implementation conflict, update the docs or explicitly report why the apparent conflict is not drift.

## Sync Workflow

### 1. Read the Repo's Documentation Contract

Start with the files that define how documentation is maintained:

- Agent instructions such as `AGENTS.md`, `CLAUDE.md`, `HERMES.md`, or equivalent.
- Collaboration/status docs such as `COLLABORATION.md`, `ROADMAP.md`, `PROJECT_LOG.md`, changelogs, release notes, or current specs.
- Architecture docs when module boundaries or ownership change.
- User-facing docs when behavior, setup, commands, configuration, or workflows change.

Follow project-local instructions over generic habits.

### 2. Establish Ground Truth

Before editing docs, find the strongest local evidence for what is true now:

- Read the changed implementation and any public API/schema/config it affects.
- Check deletions, renames, and removed examples in the diff; removals often create stale docs.
- Find one or two working examples, tests, fixtures, or generated artifacts that show the correct current pattern.
- For API or type docs, prefer the compiler, typechecker, generated declarations, schema validator, or existing executable examples over memory.

If the task starts from a doc file instead of code changes, run the same process in reverse: extract claims, paths, commands, signatures, and examples from the doc, then verify each against the current codebase.

### 3. Derive Doc Scope From the Diff

Inspect the actual changes before editing docs. Map each changed surface to likely documentation:

- User-visible behavior -> README, product docs, current collaboration/status docs, changelog.
- Public API, schema, config, CLI, environment variables -> API docs, examples, setup docs, migration notes.
- Architecture, ownership, module boundaries -> architecture docs and agent instructions.
- Release/version status -> changelog, release notes, roadmap, collaboration docs.
- Workflow or handoff rules -> agent instructions, handoff docs, lessons files.
- Visual/product changes -> note deterministic checks and defer subjective acceptance when the project requires human visual approval.

Do not update unrelated docs just to make the tree look busy.

### 4. Search for Stale Language

Before finalizing, search current docs for contradicted status:

- Future-tense descriptions of completed work.
- Old version labels or release lines.
- `next`, `todo`, `not done`, `pending`, or `blocked` text that no longer matches reality.
- Feature lists that omit the newly delivered behavior.
- Handoff instructions that still point at obsolete files, modules, or manual steps.

If stale text is found, update it or explicitly explain why it remains true.

### 5. Write Narrow, Truthful Updates

A good doc sync says both sides of the boundary:

- What changed.
- What did not change.
- What remains manual, deferred, or visually/user accepted.
- Which checks were run, when the repo normally records that.
- Any compatibility or migration notes future work needs.

Do not inflate scope. Do not describe intended future work as already delivered. Do not erase historical context unless the project treats that doc as current-only state.

### 6. Use a Risk Gate for Human-Judgment Text

Auto-update factual drift: paths, command names, version strings, signatures, option names, feature availability, links, counts, and current status.

Flag or ask before rewriting:

- Philosophy, vision, principles, or product positioning.
- Security, threat model, privacy, or trust claims beyond factual version/path fixes.
- Architecture decision rationale or historical explanations.
- Changelog entries that already shipped, except appending or correcting clearly factual mistakes according to project convention.
- User-authored narrative, tone, or subjective product language.

When a risky section is stale, say what evidence contradicts it and propose the smallest truthful edit.

### 7. Recheck Consistency

After editing docs:

- Review the diff of docs and code together.
- Confirm version/status lines agree across current docs.
- Confirm examples, file paths, commands, and module names still exist.
- Confirm changelogs or release notes are append-only when the project expects historical records.
- Confirm important docs are reachable from normal entry points when adding a new doc.
- Confirm public examples, snippets, and signatures match the current implementation or executable examples.
- Confirm final response mentions doc updates when they are part of the task.

## Stop Rules

Do not finish a repo modification when:

- Current docs still call the delivered work future or unfinished.
- The final claim relies on behavior not documented anywhere the project expects.
- A doc update would require product decisions the user has not made.
- You cannot tell which docs are authoritative; ask or state the blocker.

For no-code tasks, do not invent doc churn. Report that no repository docs were changed because the repository did not change.
