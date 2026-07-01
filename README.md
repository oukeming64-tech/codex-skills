# Codex Skills

Personal Codex skills distilled from real project work.

## Skills

- `handoff-auditor`: audit implementation handoffs before accepting, merging, or declaring them complete. It checks claims against current code, verification evidence, docs, release state, and human acceptance requirements.
- `docs-sync-guardian`: keep repository documentation aligned with code, configuration, asset, release, workflow, or product changes. It treats docs as suspicious after changes, grounds updates in live implementation evidence, and uses a risk gate for human-judgment text.

## Local Use

Copy a skill folder from `skills/` into `~/.codex/skills/`.

Current local copies are installed at:

- `~/.codex/skills/handoff-auditor`
- `~/.codex/skills/docs-sync-guardian`

## Validation

Run the fusion A/B coverage smoke check before claiming an absorbed skill update is complete:

```bash
python3 evals/fusion_ab_eval.py --old-ref 1d9949e --new-ref HEAD
```

To focus one skill:

```bash
python3 evals/fusion_ab_eval.py --old-ref 1d9949e --new-ref HEAD --skill docs-sync-guardian
```

This check catches missing fusion targets and baseline regressions. It does not replace independent review or scenario-based behavior testing.
