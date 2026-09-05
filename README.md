# Evidence-First Agent Skills

Portable agent skills distilled from real project work and maintained by
[`oukeming64-tech`](https://github.com/oukeming64-tech). The current collection
focuses on one boundary: an agent should not call work complete until its code,
evidence, documentation, release state, and stated scope agree.

## Start here

| Your task | Use |
| --- | --- |
| Update docs after changing implementation | `docs-sync-guardian` |
| Check another agent's or contributor's claimed completion | `handoff-auditor` |
| Work in an existing docs-as-memory project | Let its `doc-memory` flow own retrieval and sealing; reuse that evidence |

Choose the owner that fits the task. A small edit does not need three complete pipelines or a new documentation index.

## Skills

- `handoff-auditor`: audit implementation handoffs before accepting, merging, or declaring them complete. It checks claims against current code, verification evidence, docs, release state, and human acceptance requirements.
- `docs-sync-guardian`: keep repository documentation aligned with code, configuration, asset, release, workflow, or product changes. It treats docs as suspicious after changes, grounds updates in live implementation evidence, and uses a risk gate for human-judgment text.

Both skills are instruction-only. They add no MCP server, network client,
credential handling, telemetry, background service, or install hook.

## DeepSeek Harness

This repository includes a community, Skill-only bundle for the DeepSeek
Harness developer preview. It is not an official DeepSeek product and does not
imply DeepSeek endorsement.

Compatibility target: `@deepseek-ai/dsh@0.1.0-rc.6` with Node.js
`^22.19.0 || >=24.0.0`.

Install the tagged GitHub package into the Web profile:

```bash
dsh plugin --profile web add 'github:oukeming64-tech/codex-skills#dsh-v0.1.0'
```

Invoke either skill explicitly:

```text
Use the handoff-auditor skill to verify this completion claim before accepting it.
Use the docs-sync-guardian skill to check this change for documentation drift.
```

Uninstall:

```bash
dsh plugin --profile web remove @oukeming64-tech/codex-skills
```

The integration only registers this repository's `skills/` directory through
Harness's ordinary filesystem Skill provider. It does not add native tools or
change the default permission model.

## Other Agent Runtimes

Copy a skill folder from `skills/` into the runtime's user or project Skill
directory. For Codex, use `~/.codex/skills/` or a compatible `.agents/skills/`
location. For a Harness project-local installation, use `.dsh/skills/`.

Keep the folder name unchanged so it matches the `name` in `SKILL.md`.

## Repository Validation

Run the fusion A/B coverage smoke check before claiming an absorbed skill update is complete:

```bash
python3 evals/fusion_ab_eval.py --old-ref 1d9949e --new-ref HEAD
```

To focus one skill:

```bash
python3 evals/fusion_ab_eval.py --old-ref 1d9949e --new-ref HEAD --skill docs-sync-guardian
```

This check catches missing fusion targets and baseline regressions. It does not replace independent review or scenario-based behavior testing.

The DeepSeek Harness package contract is checked separately:

```bash
node --test dsh/test/*.test.mjs
```

## Ownership and Issues

- Author and maintainer: [`oukeming64-tech`](https://github.com/oukeming64-tech)
- Source: [`oukeming64-tech/codex-skills`](https://github.com/oukeming64-tech/codex-skills)
- Issues: [`oukeming64-tech/codex-skills/issues`](https://github.com/oukeming64-tech/codex-skills/issues)

Released under the [MIT License](LICENSE).
