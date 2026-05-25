#!/usr/bin/env python3
"""
check_originality.py
====================

Guard against verbatim copying from Jason Liu's "Codex-maxxing" essay.

What it does
------------
1. Downloads the source article (cached to ``scripts/.cache/jason-original.txt``).
2. Tokenises both the source and every tracked drop-in / skill file
   (``AGENTS.md``, ``CLAUDE.md``, ``skills/**/*.md``).
3. Builds 15-token sliding windows on each side and intersects them.
4. Any non-empty intersection is treated as a copyright red-flag:
   the script prints the offending file, line number, and snippet, then
   exits non-zero.

Design notes
------------
- **Standard library only.** No pip install in CI.
- The 15-token threshold is chosen so concept names (``durable threads``,
  ``heartbeats``, ``side panel``) and the one whitelisted 7-word quote
  ("Ambition without verification is just a wish.") cannot trigger it.
- Tokenisation lowercases, keeps hyphenated/apostrophised words intact,
  and strips everything else. This makes the check robust to punctuation
  drift while still catching real verbatim runs.
- HTML extraction skips ``script``/``style``/``nav``/``footer`` so site
  chrome can't poison the source corpus.
"""

from __future__ import annotations

import html
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

SOURCE_URL = "https://jxnl.co/writing/2026/05/10/codex-maxxing/"
NGRAM = 15

REPO_ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = REPO_ROOT / "scripts" / ".cache" / "jason-original.txt"

DIRECT_TARGETS = ("AGENTS.md", "CLAUDE.md", "README.md")
GLOB_TARGETS = ("skills/**/*.md",)

# Tags whose text content is not part of the article body.
_SKIP_TAGS = frozenset(
    {"script", "style", "noscript", "svg", "nav", "header", "footer", "aside", "form"}
)

# Word = run of letters/digits, optionally joined by - or ' to more letters/digits.
_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")


class _TextExtractor(HTMLParser):
    """Pull readable text out of HTML, skipping non-content tags."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs):  # type: ignore[override]
        if tag in _SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str):  # type: ignore[override]
        if tag in _SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str):  # type: ignore[override]
        if self._skip_depth == 0:
            self._chunks.append(data)

    def text(self) -> str:
        return " ".join(self._chunks)


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def tokenize_with_lines(text: str) -> list[tuple[str, int]]:
    """Return ``(token, 1-indexed-line-number)`` pairs."""
    out: list[tuple[str, int]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for tok in _TOKEN_RE.findall(line.lower()):
            out.append((tok, lineno))
    return out


def _fetch_source() -> str:
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "codex-maxxing-originality-ci/1.0 (+https://github.com/Edward4226/codex-maxxing)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:  # nosec: B310 — fixed https URL
        raw = resp.read().decode("utf-8", errors="replace")
    parser = _TextExtractor()
    parser.feed(raw)
    return html.unescape(parser.text())


def load_source(refresh: bool = False) -> str:
    if refresh or not CACHE_PATH.exists():
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        text = _fetch_source()
        CACHE_PATH.write_text(text, encoding="utf-8")
    return CACHE_PATH.read_text(encoding="utf-8")


def ngrams(tokens: list[str], n: int = NGRAM) -> Iterable[tuple[str, ...]]:
    for i in range(len(tokens) - n + 1):
        yield tuple(tokens[i : i + n])


def collect_target_files() -> list[Path]:
    files: set[Path] = set()
    for name in DIRECT_TARGETS:
        p = REPO_ROOT / name
        if p.exists():
            files.add(p.resolve())
    for pattern in GLOB_TARGETS:
        for p in REPO_ROOT.glob(pattern):
            if p.is_file():
                files.add(p.resolve())
    return sorted(files)


def main() -> int:
    refresh = os.environ.get("ORIGINALITY_REFRESH") == "1"

    try:
        source_text = load_source(refresh=refresh)
    except Exception as exc:  # network failure, parse failure, etc.
        print(
            f"ERROR: could not load source article from {SOURCE_URL}: {exc}",
            file=sys.stderr,
        )
        return 2

    source_tokens = tokenize(source_text)
    if len(source_tokens) < NGRAM * 4:
        print(
            f"ERROR: source corpus too small ({len(source_tokens)} tokens). "
            "Cache may be stale or fetch may have failed. "
            "Retry with ORIGINALITY_REFRESH=1.",
            file=sys.stderr,
        )
        return 2

    source_grams: set[tuple[str, ...]] = set(ngrams(source_tokens))

    targets = collect_target_files()
    if not targets:
        print("ERROR: no target files found; expected AGENTS.md/CLAUDE.md/skills/**/*.md", file=sys.stderr)
        return 2

    hits: list[tuple[Path, int, str]] = []
    for path in targets:
        rel = path.relative_to(REPO_ROOT)
        toks = tokenize_with_lines(path.read_text(encoding="utf-8"))
        bare = [t for t, _ in toks]
        for i in range(len(bare) - NGRAM + 1):
            gram = tuple(bare[i : i + NGRAM])
            if gram in source_grams:
                lineno = toks[i][1]
                hits.append((rel, lineno, " ".join(gram)))

    if hits:
        print(
            f"FAIL: found {len(hits)} 15-token overlap(s) with the source article.",
            file=sys.stderr,
        )
        print(f"Source: {SOURCE_URL}\n", file=sys.stderr)
        for rel, lineno, snippet in hits:
            print(f"  {rel}:{lineno}  …{snippet}…", file=sys.stderr)
        print(
            "\nRewrite each flagged span in your own words. "
            "Concept names <15 tokens (e.g. 'durable threads', 'heartbeats') are fine.",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {len(targets)} file(s) checked against "
        f"{len(source_grams)} source 15-grams; no overlap found."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
