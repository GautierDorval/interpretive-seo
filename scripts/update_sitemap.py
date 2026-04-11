#!/usr/bin/env python3
"""
Update <lastmod> in sitemap.xml (and public/sitemap.xml) from git mtime.

The sitemap on this repo is hand-committed. This script regenerates only
the <lastmod> values based on the real last-commit date of each URL's
source HTML file. Everything else (URL list, priorities, changefreq) is
preserved verbatim.

Runs in .github/workflows/update-sitemap.yml on every push to main, and
can also be run locally: `python3 scripts/update_sitemap.py`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://interpretive-seo.org"
SITEMAP_PATHS = [ROOT / "sitemap.xml", ROOT / "public" / "sitemap.xml"]


def build_git_mtime_cache() -> dict[str, str]:
    """Return {repo_relative_path: last_commit_date_YYYY-MM-DD} for the full repo."""
    try:
        out = subprocess.check_output(
            ["git", "-C", str(ROOT), "log", "--name-only", "--pretty=format:__COMMIT__%cs"],
            text=True,
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        print(f"[sitemap] git log failed: {err}", file=sys.stderr)
        return {}
    cache: dict[str, str] = {}
    current_date: str | None = None
    for raw_line in out.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("__COMMIT__"):
            current_date = line[len("__COMMIT__") :]
        elif current_date and line not in cache:
            cache[line] = current_date
    return cache


def url_to_file_candidates(url: str) -> list[str]:
    """Return plausible source file paths for a sitemap URL.

    Tries leaf .html first (e.g. /definition -> definition.html), then
    directory index (/context/ -> context/index.html).
    """
    path = url.replace(SITE_URL, "")
    if path in ("", "/"):
        return ["index.html"]
    path = path.lstrip("/").rstrip("/")
    return [f"{path}.html", f"{path}/index.html"]


def resolve_mtime(url: str, cache: dict[str, str]) -> str | None:
    for candidate in url_to_file_candidates(url):
        if candidate in cache:
            return cache[candidate]
    return None


URL_BLOCK_RE = re.compile(r"<url>[\s\S]*?</url>")
LOC_RE = re.compile(r"<loc>([^<]+)</loc>")
LASTMOD_RE = re.compile(r"<lastmod>[^<]+</lastmod>")


def rewrite_sitemap(path: Path, cache: dict[str, str], stats: dict[str, int]) -> bool:
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")

    def rewrite_block(match: re.Match) -> str:
        block = match.group(0)
        loc_match = LOC_RE.search(block)
        if not loc_match:
            return block
        url = loc_match.group(1)
        new_mtime = resolve_mtime(url, cache)
        if not new_mtime:
            stats["unresolved"] += 1
            return block
        new_lastmod = f"<lastmod>{new_mtime}</lastmod>"
        if LASTMOD_RE.search(block):
            updated = LASTMOD_RE.sub(new_lastmod, block)
            if updated != block:
                stats["updated"] += 1
            else:
                stats["unchanged"] += 1
            return updated
        stats["inserted"] += 1
        return block.replace(
            loc_match.group(0),
            f"{loc_match.group(0)}\n    {new_lastmod}",
            1,
        )

    new_content = URL_BLOCK_RE.sub(rewrite_block, content)
    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main() -> int:
    cache = build_git_mtime_cache()
    print(f"[sitemap] git mtime cache: {len(cache)} files")
    stats = {"updated": 0, "unchanged": 0, "inserted": 0, "unresolved": 0}
    changed_any = False
    for path in SITEMAP_PATHS:
        if rewrite_sitemap(path, cache, stats):
            print(f"[sitemap] rewrote {path.relative_to(ROOT)}")
            changed_any = True
    print(
        f"[sitemap] entries: {stats['updated']} updated, "
        f"{stats['unchanged']} unchanged, {stats['inserted']} inserted, "
        f"{stats['unresolved']} unresolved"
    )
    if not changed_any:
        print("[sitemap] no changes required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
