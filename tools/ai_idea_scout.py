#!/usr/bin/env python3
"""
ai_idea_scout.py - Have an OpenAI model scout for net-new RDX feature ideas
and propose them as GitHub issues.

Reads the repo's current state (README, REQUIREMENTS.md, CLAUDE.md, methodology
docs) plus the list of currently open GitHub issues, then asks an OpenAI model
with the native ``web_search`` tool to propose 1-5 feature ideas grounded in
recent activity in OWASP CycloneDX, ISO/SAE 21434, ISO/SAE PAS 8475, UNECE
WP.29 R155/R156, ENISA, Auto-ISAC, NIST SSDF, and adjacent ecosystems. Each
proposal becomes a GitHub issue (via ``gh issue create``) labeled
``ai-proposal`` for human triage.

Usage:
    OPENAI_API_KEY=sk-... \\
        python tools/ai_idea_scout.py \\
            --repo-root . \\
            --existing-issues issues.json \\
            --dry-run

    OPENAI_API_KEY=sk-... GH_TOKEN=... \\
        python tools/ai_idea_scout.py \\
            --repo-root . \\
            --existing-issues issues.json \\
            --create-issues
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5"
DEFAULT_LABELS = ["ai-proposal", "enhancement"]

# Files we pass to the model as repo context. Missing files are skipped silently.
REPO_CONTEXT_FILES = [
    "README.md",
    "REQUIREMENTS.md",
    "CLAUDE.md",
    "VERSIONING.md",
    "CONTRIBUTING.md",
    "methodology/Methodology.md",
    "methodology/ISO21434-Mapping.md",
    "methodology/CAL-TAF-Integration.md",
    "methodology/UseCases.md",
    "methodology/XSAM-Gap-Analysis.md",
]

SYSTEM_PROMPT = """You are a TARA / automotive cybersecurity standards analyst helping to evolve
the Risk Data Exchange (RDX) project — an open, vendor-neutral format for
exchanging automotive cybersecurity risk data, aligned with ISO/SAE 21434 and
based on CycloneDX.

Your job: propose 1 to 5 net-new feature ideas the project could adopt,
grounded in recent activity in adjacent standards and ecosystems. You MUST
search the web for fresh context before proposing — favor sources such as:

  * OWASP CycloneDX (cyclonedx.org, GitHub releases, RFC repositories,
    new property taxonomies, BOV / CSAF / VEX / ML-BOM intersections)
  * ISO/SAE 21434 (Road vehicles — Cybersecurity engineering)
  * ISO/SAE PAS 8475 (CAL and TAF framework)
  * UNECE WP.29 R155 / R156
  * ENISA automotive cybersecurity reports
  * Auto-ISAC publications
  * NIST SP 800-160 Vol. 2, SSDF (SP 800-218), SP 800-161 (C-SCRM)
  * Open-source TARA tooling

Quality bar:
  * Each proposal must be concrete enough that a maintainer can scope it,
    estimate it, and either accept or reject it on the merits.
  * Proposals MUST NOT duplicate any currently open issue (you will be
    given the list) and SHOULD NOT duplicate capabilities already covered
    in REQUIREMENTS.md.
  * Prefer additive, backwards-compatible schema or tooling improvements.
  * Cite at least one external source per proposal (URL).
  * Map each proposal to existing RDX requirement IDs (RDX-XXX) where it
    extends or relates to one, and note "(new requirement)" otherwise.

Output format: a JSON array (and nothing else — no prose, no markdown
fences) where each element has exactly these fields:

  * "title":  short imperative issue title (< 80 chars)
  * "body":   markdown body with these sections, in this order:
                "## Motivation"
                "## Proposed change"
                "## References"
                "## Acceptance criteria"
              The body should be specific enough that a contributor could
              open a PR implementing it without further clarification.
  * "labels": array of strings to apply (always include "ai-proposal")
  * "source_urls": array of URLs you actually consulted

If after research you cannot find anything net-new that meets the quality
bar, return an empty array [].
"""


def load_repo_context(repo_root: Path, max_chars_per_file: int = 20000) -> str:
    parts = []
    for rel in REPO_CONTEXT_FILES:
        f = repo_root / rel
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars_per_file:
            text = text[:max_chars_per_file] + "\n...[truncated]..."
        parts.append(f"### {rel}\n\n{text}\n")

    for d in ("examples", "spec", "templates"):
        sub = repo_root / d
        if sub.exists():
            entries = sorted(
                str(p.relative_to(repo_root))
                for p in sub.rglob("*")
                if p.is_file()
            )
            parts.append(
                f"### `{d}/` contents\n\n" + "\n".join(f"- {e}" for e in entries)
            )
    return "\n\n".join(parts)


def load_existing_issues(path):
    if path is None or not path.exists():
        return "(no open issues file provided)"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"(could not parse existing issues: {exc})"
    if not raw:
        return "(no open issues)"
    lines = []
    for it in raw:
        labels = ",".join(lab.get("name", "") for lab in it.get("labels", []))
        title = it.get("title", "")
        num = it.get("number", "?")
        lines.append(f"- #{num} [{labels}] {title}")
    return "\n".join(lines)


def call_openai(api_key: str, model: str, prompt: str) -> str:
    body = {
        "model": model,
        "tools": [{"type": "web_search"}],
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        OPENAI_API_URL,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        sys.stderr.write(f"OpenAI API error {exc.code}: {err_body}\n")
        raise

    if payload.get("output_text"):
        return payload["output_text"]

    texts = []
    for item in payload.get("output", []):
        for c in item.get("content", []):
            if c.get("type") in ("output_text", "text"):
                texts.append(c.get("text", ""))
    return "".join(texts)


def parse_proposals(text: str) -> list:
    text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        try:
            data = json.loads(fence.group(1))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass

    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end > start:
        try:
            data = json.loads(text[start : end + 1])
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Could not parse a JSON array of proposals from model output. "
        "First 500 chars:\n" + text[:500]
    )


def make_issue_body(proposal: dict) -> str:
    body = (proposal.get("body") or "").rstrip()
    sources = proposal.get("source_urls") or []
    if sources and "## References" not in body:
        body += "\n\n## References\n" + "\n".join(f"- {u}" for u in sources)
    body += (
        "\n\n---\n"
        "_Generated by `tools/ai_idea_scout.py` via the AI Idea Scout workflow._\n"
        "_Review the proposal, refine the title/body/labels, and close if not desired._"
    )
    return body


def create_issue(title: str, body: str, labels) -> str:
    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for lab in labels:
        cmd += ["--label", lab]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(f"gh issue create failed: {result.stderr}\n")
        if "label" in (result.stderr or "").lower():
            retry = subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body", body],
                capture_output=True,
                text=True,
            )
            if retry.returncode == 0:
                return retry.stdout.strip()
            sys.stderr.write(
                f"retry without labels failed: {retry.stderr}\n"
            )
        return ""
    return result.stdout.strip()


def write_step_summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument(
        "--existing-issues",
        type=Path,
        default=None,
        help="path to JSON from `gh issue list --json number,title,labels`",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="write parsed proposals as JSON here",
    )
    parser.add_argument(
        "--create-issues",
        action="store_true",
        help="actually call `gh issue create` for each proposal",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print proposals, do not create issues",
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY environment variable is required")

    repo_ctx = load_repo_context(args.repo_root)
    issues_ctx = load_existing_issues(args.existing_issues)

    user_prompt = (
        "# Repository context\n\n"
        f"{repo_ctx}\n\n"
        "# Currently open issues (do not duplicate)\n\n"
        f"{issues_ctx}\n\n"
        "Now do your research and emit the JSON array of proposals as "
        "specified in the system prompt."
    )

    raw = call_openai(api_key, args.model, user_prompt)
    proposals = parse_proposals(raw)

    if args.output:
        args.output.write_text(json.dumps(proposals, indent=2), encoding="utf-8")

    if not proposals:
        print("No proposals generated this run.")
        write_step_summary("AI idea scout ran but produced no proposals.\n")
        return

    summary_lines = [f"AI idea scout produced {len(proposals)} proposal(s):\n"]

    for prop in proposals:
        title = (prop.get("title") or "").strip()
        if not title:
            sys.stderr.write("Skipping proposal with empty title\n")
            continue

        labels = list(prop.get("labels") or [])
        for default in DEFAULT_LABELS:
            if default not in labels:
                labels.append(default)
        body = make_issue_body(prop)

        if args.dry_run or not args.create_issues:
            print(f"\n=== {title} ===")
            print(f"[labels: {','.join(labels)}]")
            print(body)
            summary_lines.append(f"- (dry-run) **{title}**")
        else:
            url = create_issue(title, body, labels)
            if url:
                print(f"Created: {url}")
                summary_lines.append(f"- [{title}]({url})")
            else:
                summary_lines.append(f"- (failed) {title}")

    write_step_summary("\n".join(summary_lines) + "\n")


if __name__ == "__main__":
    main()
