#!/usr/bin/env python3
"""Copy an example profile (site.config + links + archive) into the active config/data dirs.

USAGE
-----
  scripts/apply-example.py --name ernestyalumni
  scripts/apply-example.py --name sample-creator
  scripts/apply-example.py --list

Files in `examples/<name>/` overwrite:
  - examples/<name>/site.config.json -> config/site.config.json
  - examples/<name>/links.json       -> data/links.json
  - examples/<name>/archive.json     -> data/archive.json   (only if it exists)
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples"


def list_examples() -> int:
    for d in sorted(p for p in EXAMPLES.iterdir() if p.is_dir()):
        cfg = d / "site.config.json"
        marker = "✓" if cfg.exists() else "✗"
        print(f"  {marker} {d.name}")
    return 0


def apply(name: str) -> int:
    src = EXAMPLES / name
    if not src.is_dir():
        print(f"error: example '{name}' not found in {EXAMPLES}", file=sys.stderr)
        return 2

    pairs = [
        (src / "site.config.json", REPO / "config" / "site.config.json"),
        (src / "links.json",       REPO / "data" / "links.json"),
        (src / "archive.json",     REPO / "data" / "archive.json"),
    ]
    copied = 0
    for s, d in pairs:
        if not s.exists():
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(s, d)
        print(f"  copied {s.relative_to(REPO)} -> {d.relative_to(REPO)}")
        copied += 1
    if copied == 0:
        print(f"warn: no files found in {src}", file=sys.stderr)
        return 1
    print(f"\napplied example '{name}' ({copied} files). Run `npm run build` to verify.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Apply an example profile.")
    p.add_argument("--name", help="Example name (folder under examples/)")
    p.add_argument("--list", action="store_true", help="List available examples")
    args = p.parse_args()

    if args.list:
        return list_examples()
    if not args.name:
        p.print_help()
        return 2
    return apply(args.name)


if __name__ == "__main__":
    sys.exit(main())
