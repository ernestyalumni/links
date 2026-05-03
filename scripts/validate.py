#!/usr/bin/env python3
"""Validate config/site.config.json and data/links.json without external deps.

Checks performed:
  • Both files parse as JSON.
  • Site config has required {site.title, site.description, site.url, profile.display_name, theme}.
  • Links: every entry has unique `id`, valid kebab-case slug, non-empty title, http(s) URL.
  • Positions are unique integers ≥ 1.
  • No links share the same URL (warn, not error).

Exit codes:
  0 = all good
  1 = warnings only
  2 = at least one error
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
SITE_CFG = REPO / "config" / "site.config.json"
LINKS = REPO / "data" / "links.json"
ARCHIVE = REPO / "data" / "archive.json"

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,59}$")


def err(msg: str): print(f"  ✗ {msg}", file=sys.stderr)
def warn(msg: str): print(f"  ! {msg}")
def ok(msg: str): print(f"  ✓ {msg}")


def validate_site_config() -> list[str]:
    errors: list[str] = []
    print(f"\n[ {SITE_CFG.relative_to(REPO)} ]")
    if not SITE_CFG.exists():
        errors.append("site.config.json missing")
        err("missing")
        return errors
    try:
        cfg = json.loads(SITE_CFG.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"invalid JSON: {e}")
        err(f"invalid JSON: {e}")
        return errors

    site = cfg.get("site", {})
    profile = cfg.get("profile", {})
    theme = cfg.get("theme", {})

    for k in ("title", "description", "url"):
        if not site.get(k):
            errors.append(f"site.{k} required")
            err(f"site.{k} required")
    if not profile.get("display_name"):
        errors.append("profile.display_name required")
        err("profile.display_name required")

    preset = theme.get("preset", "academic")
    valid_presets = {"academic", "minimal", "terminal", "dark-space"}
    if preset not in valid_presets:
        errors.append(f"theme.preset='{preset}' not in {valid_presets}")
        err(f"theme.preset='{preset}' not in {valid_presets}")

    color_scheme = theme.get("color_scheme", "auto")
    if color_scheme not in {"light", "dark", "auto"}:
        errors.append(f"theme.color_scheme='{color_scheme}' invalid")
        err(f"theme.color_scheme='{color_scheme}' invalid")

    if not errors:
        ok(f"site config valid (theme={preset}, scheme={color_scheme})")
    return errors


def validate_links_file(path: Path, label: str, require_position: bool) -> list[str]:
    errors: list[str] = []
    print(f"\n[ {path.relative_to(REPO)} ]")
    if not path.exists():
        if label == "links":
            errors.append(f"{path.name} missing")
            err("missing")
        else:
            ok("missing (optional)")
        return errors
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"invalid JSON: {e}")
        err(f"invalid JSON: {e}")
        return errors

    links = data.get("links", [])
    if not isinstance(links, list):
        errors.append("'links' is not a list")
        err("'links' is not a list")
        return errors

    ids: set[str] = set()
    positions: set[int] = set()
    urls: dict[str, str] = {}

    for i, l in enumerate(links):
        ctx = f"links[{i}]"
        if not isinstance(l, dict):
            errors.append(f"{ctx} is not an object")
            err(f"{ctx} is not an object")
            continue
        lid = l.get("id", "")
        title = l.get("title", "")
        url = l.get("url", "")

        if not lid or not SLUG_RE.match(lid):
            errors.append(f"{ctx} invalid id '{lid}'")
            err(f"{ctx} invalid id '{lid}' (kebab-case 1-60 chars)")
        elif lid in ids:
            errors.append(f"{ctx} duplicate id '{lid}'")
            err(f"{ctx} duplicate id '{lid}'")
        else:
            ids.add(lid)

        if not title:
            errors.append(f"{ctx} title required")
            err(f"{ctx} ({lid}) title required")

        if not url:
            errors.append(f"{ctx} url required")
            err(f"{ctx} ({lid}) url required")
        else:
            try:
                u = urlparse(url)
                if u.scheme not in {"http", "https"}:
                    errors.append(f"{ctx} url scheme not http(s)")
                    err(f"{ctx} ({lid}) url not http(s): {url}")
                if not u.netloc:
                    errors.append(f"{ctx} url missing host")
                    err(f"{ctx} ({lid}) url missing host: {url}")
                if url in urls:
                    warn(f"{ctx} ({lid}) duplicate URL with '{urls[url]}'")
                else:
                    urls[url] = lid
            except Exception as e:
                errors.append(f"{ctx} url parse failed: {e}")
                err(f"{ctx} ({lid}) url parse failed: {e}")

        if require_position:
            pos = l.get("position")
            if not isinstance(pos, int) or pos < 1:
                errors.append(f"{ctx} ({lid}) position must be positive int")
                err(f"{ctx} ({lid}) position must be positive int")
            elif pos in positions:
                errors.append(f"{ctx} ({lid}) duplicate position {pos}")
                err(f"{ctx} ({lid}) duplicate position {pos}")
            else:
                positions.add(pos)

    if not errors:
        ok(f"{label}: {len(links)} entries valid")
    return errors


def main() -> int:
    print("Validating links project…")
    errs = []
    errs += validate_site_config()
    errs += validate_links_file(LINKS, "links", require_position=True)
    errs += validate_links_file(ARCHIVE, "archive", require_position=False)
    print()
    if errs:
        print(f"FAIL: {len(errs)} error(s)", file=sys.stderr)
        return 2
    print("OK — project is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
