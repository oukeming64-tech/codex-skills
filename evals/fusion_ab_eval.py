#!/usr/bin/env python3
"""Deterministic old-vs-new smoke checks for workflow-skill fusion.

This is not a model-quality benchmark and does not prove behavior quality. It is
a coverage/regression smoke harness for the specific capabilities this
repository expects a fusion to preserve or improve.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SKILL_PATHS = {
    "handoff-auditor": "skills/handoff-auditor/SKILL.md",
    "docs-sync-guardian": "skills/docs-sync-guardian/SKILL.md",
}


@dataclass(frozen=True)
class Case:
    skill: str
    category: str
    name: str
    patterns: tuple[str, ...]
    anti_patterns: tuple[str, ...] = ()


CASES: tuple[Case, ...] = (
    Case(
        "handoff-auditor",
        "fusion-target",
        "evidence hierarchy rejects unsupported handoff summaries",
        (r"trust order", r"handoff author", r"summary loses"),
        (r"handoff author(?:'s)? summary wins", r"trust the handoff author over"),
    ),
    Case(
        "handoff-auditor",
        "fusion-target",
        "worktree safety protects user-owned changes",
        (r"Worktree Safety Preflight", r"HEAD", r"reset|discard|stash"),
        (r"ignore worktree safety", r"stash.*without.*approval", r"reset --hard"),
    ),
    Case(
        "handoff-auditor",
        "fusion-target",
        "remote, release, tag, and PR claims require direct verification",
        (r"pushed|tagged|released|PR state", r"remote state"),
    ),
    Case(
        "handoff-auditor",
        "fusion-target",
        "evidence matrix exposes unknown surfaces",
        (r"Evidence Matrix", r"Unknown is not `N/A`"),
    ),
    Case(
        "handoff-auditor",
        "fusion-target",
        "human or visual acceptance can block handoff acceptance",
        (r"Human acceptance", r"visual|product"),
    ),
    Case(
        "handoff-auditor",
        "baseline-regression",
        "stale current docs block completion claims",
        (r"stale", r"blocked|blocks acceptance", r"future|unfinished"),
    ),
    Case(
        "handoff-auditor",
        "baseline-regression",
        "verification gaps and unchecked edge cases must be named",
        (r"Verification", r"gaps|unchecked edge cases"),
    ),
    Case(
        "handoff-auditor",
        "baseline-regression",
        "historical docs are not loaded by default",
        (r"Do not load every historical document",),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "documentation is suspicious until implementation is checked",
        (r"documentation is suspicious", r"aggressive.*searching.*conservative.*editing"),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "implementation, API, and executable examples outrank docs",
        (r"trust order", r"Working implementation", r"Documentation"),
        (r"documentation always outranks implementation",),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "ground-truth pass checks changed implementation and removals",
        (r"Establish Ground Truth", r"removals|renames|removed examples"),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "doc-to-code reverse verification is supported",
        (r"starts from a doc file", r"verify each against the current codebase"),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "compiler, typechecker, declarations, or schema validators are preferred for API docs",
        (r"compiler|typechecker", r"schema validator|generated declarations"),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "risk gate protects human-judgment text",
        (r"Risk Gate", r"Philosophy|vision|principles", r"Security|threat model"),
        (r"silently rewrite security policy to match implementation", r"silently rewrite product contracts to match implementation"),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "normative docs and policies are flagged instead of silently rewritten",
        (r"normative spec|security policy|product contract", r"do not silently rewrite", r"ask which source should change"),
    ),
    Case(
        "docs-sync-guardian",
        "fusion-target",
        "reachability and public snippets are rechecked",
        (r"reachable", r"examples, snippets, and signatures"),
    ),
    Case(
        "docs-sync-guardian",
        "baseline-regression",
        "doc updates state what changed and what did not change",
        (r"What changed", r"What did not change"),
    ),
    Case(
        "docs-sync-guardian",
        "baseline-regression",
        "unrelated documentation churn is rejected",
        (r"Do not update unrelated docs",),
    ),
    Case(
        "docs-sync-guardian",
        "baseline-regression",
        "stale future-tense and pending language is searched",
        (r"Future-tense", r"`next`, `todo`, `not done`, `pending`, or `blocked`"),
    ),
)


def run_git_show(repo: Path, rev: str, rel_path: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{rev}:{rel_path}"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def load_skill(repo: Path, rev: str, skill: str) -> str:
    rel_path = SKILL_PATHS[skill]
    if rev == "working-tree":
        return (repo / rel_path).read_text()
    return run_git_show(repo, rev, rel_path)


def match_case(text: str, case: Case) -> bool:
    required = all(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in case.patterns)
    forbidden = any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in case.anti_patterns)
    return required and not forbidden


def score(cases: list[Case], texts: dict[str, str]) -> tuple[int, list[tuple[Case, bool]]]:
    results: list[tuple[Case, bool]] = []
    for case in cases:
        ok = match_case(texts[case.skill], case)
        results.append((case, ok))
    return sum(ok for _, ok in results), results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--old-ref", default="1d9949e", help="Old git ref")
    parser.add_argument("--new-ref", default="HEAD", help="New git ref or 'working-tree'")
    parser.add_argument(
        "--skill",
        choices=sorted(SKILL_PATHS),
        help="Evaluate only one skill instead of the full fusion set",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    selected_skills = [args.skill] if args.skill else list(SKILL_PATHS)
    old_texts = {skill: load_skill(repo, args.old_ref, skill) for skill in selected_skills}
    new_texts = {skill: load_skill(repo, args.new_ref, skill) for skill in selected_skills}

    by_skill = {skill: [case for case in CASES if case.skill == skill] for skill in selected_skills}

    failed = False
    print(f"A/B fusion eval: old={args.old_ref} new={args.new_ref}")

    for skill, cases in by_skill.items():
        old_score, old_results = score(cases, old_texts)
        new_score, new_results = score(cases, new_texts)
        print(f"\n== {skill} ==")
        print(f"old score: {old_score}/{len(cases)}")
        print(f"new score: {new_score}/{len(cases)}")

        for case, old_ok in old_results:
            new_ok = dict((c.name, ok) for c, ok in new_results)[case.name]
            marker = "PASS" if new_ok else "FAIL"
            delta = "gained" if new_ok and not old_ok else "kept" if new_ok else "missing"
            print(f"[{marker}] {case.category}: {case.name} ({delta})")

            if case.category == "baseline-regression" and old_ok and not new_ok:
                failed = True
                print(f"  regression: old passed but new failed")
            if case.category == "fusion-target" and not new_ok:
                failed = True
                print(f"  fusion target missing in new version")

        if new_score <= old_score:
            failed = True
            print("  failure: new version did not improve total score")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
