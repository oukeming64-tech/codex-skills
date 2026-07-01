---
name: handoff-auditor
description: Audit implementation handoffs before accepting, merging, or declaring them complete. Use when Codex reviews another agent's claimed completion, a PR or branch handoff, release readiness, "done" status, or any feature where code, tests, docs, edge cases, and product acceptance must agree. Especially useful for agent-to-agent workflows such as Hermes/Claude handoffs where build success alone is not enough.
---

# Handoff Auditor

## Overview

Review a handoff as a claim that must be proven across code, behavior, documentation, and stated scope. Start by looking for contradictions; accept only when the repository state supports the claimed status.

## Core Rule

No evidence, no acceptance. A handoff is ready only when the current repository state, verification output, documentation, and stated scope all support the same conclusion.

Use this trust order:

1. Current working tree, diff, branch, and `HEAD`.
2. Running implementation, tests, build, typecheck, screenshots, or other live verification.
3. Current project docs, specs, release notes, and handoff notes.
4. The handoff author's summary.

When these conflict, the handoff author's summary loses.

## Audit Workflow

### 1. Worktree Safety Preflight

Before reviewing, capture the current branch and worktree state. Treat modified, staged, and untracked files as possibly user-owned work.

- Read branch, `HEAD`, and dirty state before drawing conclusions.
- Do not move, stash, clean, overwrite, reset, or discard files while auditing.
- If the checkout contains unrelated changes, keep them out of the acceptance decision unless they affect the claimed work.
- If a claim depends on pushed, tagged, released, or PR state, verify that remote state directly instead of assuming local state implies it.

### 2. Establish the Claim

Identify exactly what the handoff says is done:

- Feature or fix name.
- Claimed user-visible behavior.
- Files or subsystems touched.
- Tests, screenshots, builds, or manual checks claimed.
- Explicit non-goals or deferred work.

If the claim is vague, infer the smallest reasonable scope from the diff and docs, then call out the assumption.

### 3. Read the Local Contract

Before judging the handoff, read the project entry instructions that define "done":

- Agent instructions such as `AGENTS.md`, `CLAUDE.md`, `HERMES.md`, or equivalent.
- Current collaboration/status docs such as `COLLABORATION.md`, `ROADMAP.md`, project logs, specs, or release notes.
- Architecture docs for changed modules.
- The directly relevant spec for touched files.

Do not load every historical document by default. Load old specs only when the current docs point there or the diff touches their completed area.

### 4. Compare Claim to Diff

Inspect the changed files and classify each change:

- Intended implementation.
- Required supporting change.
- Test or verification artifact.
- Documentation/status update.
- Unrelated or surprising change.

If unrelated changes are present, do not silently accept them. Separate them in the review or ask for scope clarification.

### 5. Search for Stale Status

Search current docs and handoff files for words that contradict the completion claim:

- `next`, `todo`, `not done`, `unfinished`, `pending`, `blocked`, `known issue`.
- Previous version labels that imply the feature is still future work.
- Old roadmap bullets that describe the delivered behavior as upcoming.
- Handoff notes that omit edge cases or verification evidence.

Completion is blocked when current docs still describe the delivered work as future, unfinished, or unaccepted.

### 6. Check Behavior and Edge Cases

Run the most relevant deterministic checks available, then reason through edge cases the checks do not cover.

For code handoffs, prefer:

- Existing test suites or targeted tests near the changed code.
- Typecheck, lint, or build when they are part of the repo's normal confidence path.
- Browser/screenshot/manual visual checks for UI, rendering, layout, or animation behavior.
- Data migration, serialization, preset, snapshot, and backward compatibility checks when data shape changes.

Name unchecked edge cases explicitly. Do not imply that a build proves visual quality, product feel, or manual acceptance.

### 7. Fill the Evidence Matrix

Before deciding, make the missing evidence visible:

| Surface | Evidence to collect | Blocks acceptance when |
|---|---|---|
| Scope | handoff claim, diff, touched files | diff includes unexplained scope or omits claimed work |
| Implementation | current code, runtime behavior, tests | code does not implement the claim or regresses adjacent behavior |
| Verification | commands, screenshots, CI, manual checks | required checks did not run or failed |
| Documentation | current docs, specs, release notes | docs still describe the work as future, unfinished, or different |
| Data/compatibility | migrations, saved data, schemas, presets, public API | changed shapes are undocumented or unverified |
| Release/remote | branch, PR, tag, artifact, published surface | claimed shipped state is not visible remotely |
| Human acceptance | user/product/visual approval notes | the project requires subjective approval and it has not happened |

Use `N/A` only when the surface truly does not apply. Unknown is not `N/A`.

### 8. Decide

Lead with findings:

- Block acceptance for real defects, stale docs, missing required verification, scope mismatch, or regressions.
- Accept with caveats only when the caveats are outside the claimed scope and are clearly documented.
- Accept when code, docs, tests/checks, and claimed scope agree.

When accepting, summarize the evidence briefly. When blocking, include the smallest concrete fix needed for acceptance.

## Review Output Shape

Use this order:

1. Findings, highest severity first, with file and line references when possible.
2. Open questions or assumptions.
3. Compact evidence matrix summary, including unknowns, when the review is not trivial.
4. Verification run and gaps.
5. Acceptance decision.

Keep summaries secondary. The point is to decide whether the handoff is actually ready, not to congratulate the existence of a diff.

If the handoff is itself a written handoff document, audit it against the repository. Do not accept a polished handoff note when the repo, docs, or remote state contradict it.
