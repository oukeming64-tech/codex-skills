---
name: handoff-auditor
description: Audit implementation handoffs before accepting, merging, or declaring them complete. Use when Codex reviews another agent's claimed completion, a PR or branch handoff, release readiness, "done" status, or any feature where code, tests, docs, edge cases, and product acceptance must agree. Especially useful for agent-to-agent workflows such as Hermes/Claude handoffs where build success alone is not enough.
---

# Handoff Auditor

## Overview

Review a handoff as a claim that must be proven across code, behavior, documentation, and stated scope. Start by looking for contradictions; accept only when the repository state supports the claimed status.

## Audit Workflow

### 1. Establish the Claim

Identify exactly what the handoff says is done:

- Feature or fix name.
- Claimed user-visible behavior.
- Files or subsystems touched.
- Tests, screenshots, builds, or manual checks claimed.
- Explicit non-goals or deferred work.

If the claim is vague, infer the smallest reasonable scope from the diff and docs, then call out the assumption.

### 2. Read the Local Contract

Before judging the handoff, read the project entry instructions that define "done":

- Agent instructions such as `AGENTS.md`, `CLAUDE.md`, `HERMES.md`, or equivalent.
- Current collaboration/status docs such as `COLLABORATION.md`, `ROADMAP.md`, project logs, specs, or release notes.
- Architecture docs for changed modules.
- The directly relevant spec for touched files.

Do not load every historical document by default. Load old specs only when the current docs point there or the diff touches their completed area.

### 3. Compare Claim to Diff

Inspect the changed files and classify each change:

- Intended implementation.
- Required supporting change.
- Test or verification artifact.
- Documentation/status update.
- Unrelated or surprising change.

If unrelated changes are present, do not silently accept them. Separate them in the review or ask for scope clarification.

### 4. Search for Stale Status

Search current docs and handoff files for words that contradict the completion claim:

- `next`, `todo`, `not done`, `unfinished`, `pending`, `blocked`, `known issue`.
- Previous version labels that imply the feature is still future work.
- Old roadmap bullets that describe the delivered behavior as upcoming.
- Handoff notes that omit edge cases or verification evidence.

Completion is blocked when current docs still describe the delivered work as future, unfinished, or unaccepted.

### 5. Check Behavior and Edge Cases

Run the most relevant deterministic checks available, then reason through edge cases the checks do not cover.

For code handoffs, prefer:

- Existing test suites or targeted tests near the changed code.
- Typecheck, lint, or build when they are part of the repo's normal confidence path.
- Browser/screenshot/manual visual checks for UI, rendering, layout, or animation behavior.
- Data migration, serialization, preset, snapshot, and backward compatibility checks when data shape changes.

Name unchecked edge cases explicitly. Do not imply that a build proves visual quality, product feel, or manual acceptance.

### 6. Decide

Lead with findings:

- Block acceptance for real defects, stale docs, missing required verification, scope mismatch, or regressions.
- Accept with caveats only when the caveats are outside the claimed scope and are clearly documented.
- Accept when code, docs, tests/checks, and claimed scope agree.

When accepting, summarize the evidence briefly. When blocking, include the smallest concrete fix needed for acceptance.

## Review Output Shape

Use this order:

1. Findings, highest severity first, with file and line references when possible.
2. Open questions or assumptions.
3. Verification run and gaps.
4. Acceptance decision.

Keep summaries secondary. The point is to decide whether the handoff is actually ready, not to congratulate the existence of a diff.
