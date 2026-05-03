#!/usr/bin/env python3
"""Edit data/links.json from the CLI. Used by sub-agents and humans alike.

USAGE
-----
  scripts/links.py list
  scripts/links.py add --title "..." --url "..." [--icon "📄"] [--tags a,b] [--position 1]
  scripts/links.py edit --id <slug> [--title ...] [--url ...] [--icon ...] [--position ...]
  scripts/links.py archive --id <slug> [--reason "..."]
  scripts/links.py reorder --order id1,id2,id3,...
  scripts/links.py move --id <slug> --to <position>

All operations rewrite data/links.json (and data/archive.json on archive)
in stable, sorted JSON. Auto-commit is the caller's responsibility.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LINKS_PATH = REPO / "data" / "links.json"
ARCHIVE_PATH = REPO / "data" / "archive.json"


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60] or "link"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def renumber(links: list[dict]) -> None:
    """Re-assign positions 1..N in current sorted order."""
    links.sort(key=lambda l: l.get("position", 9999))
    for i, l in enumerate(links, start=1):
        l["position"] = i


def cmd_list(args) -> int:
    data = load(LINKS_PATH)
    links = sorted(data.get("links", []), key=lambda l: l.get("position", 9999))
    if not links:
        print("(no links)")
        return 0
    for l in links:
        tags = ",".join(l.get("tags") or [])
        print(f"{l.get('position', '?'):>2}. [{l['id']}]  {l['title']}")
        print(f"     {l['url']}")
        if tags:
            print(f"     tags: {tags}")
    return 0


def cmd_add(args) -> int:
    data = load(LINKS_PATH)
    links = data.setdefault("links", [])
    lid = args.id or slugify(args.title)
    if any(l["id"] == lid for l in links):
        print(f"error: id '{lid}' already exists. Pass --id to override.", file=sys.stderr)
        return 2
    pos = args.position if args.position is not None else (len(links) + 1)
    new = {
        "id": lid,
        "title": args.title,
        "url": args.url,
        "icon": args.icon or "",
        "tags": [t.strip() for t in (args.tags or "").split(",") if t.strip()],
        "position": pos,
        "added_at": date.today().isoformat(),
    }
    if args.click_estimate is not None:
        new["click_estimate"] = args.click_estimate
    # Shift others down if needed
    for l in links:
        if l["position"] >= pos:
            l["position"] += 1
    links.append(new)
    renumber(links)
    save(LINKS_PATH, data)
    print(f"added: {lid} at position {new['position']}")
    return 0


def cmd_edit(args) -> int:
    data = load(LINKS_PATH)
    links = data.get("links", [])
    target = next((l for l in links if l["id"] == args.id), None)
    if not target:
        print(f"error: id '{args.id}' not found", file=sys.stderr)
        return 2
    if args.title is not None: target["title"] = args.title
    if args.url is not None: target["url"] = args.url
    if args.icon is not None: target["icon"] = args.icon
    if args.tags is not None: target["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    if args.position is not None:
        # Pull out, reinsert at new position
        old_pos = target["position"]
        for l in links:
            if l is target: continue
            if old_pos < args.position and old_pos < l["position"] <= args.position:
                l["position"] -= 1
            elif old_pos > args.position and args.position <= l["position"] < old_pos:
                l["position"] += 1
        target["position"] = args.position
        renumber(links)
    save(LINKS_PATH, data)
    print(f"edited: {args.id}")
    return 0


def cmd_archive(args) -> int:
    data = load(LINKS_PATH)
    links = data.get("links", [])
    target = next((l for l in links if l["id"] == args.id), None)
    if not target:
        print(f"error: id '{args.id}' not found in active links", file=sys.stderr)
        return 2
    archive = load(ARCHIVE_PATH) if ARCHIVE_PATH.exists() else {"links": []}
    archive_entry = dict(target)
    archive_entry["archived_at"] = date.today().isoformat()
    if args.reason:
        archive_entry["archive_reason"] = args.reason
    archive["links"].append(archive_entry)
    links.remove(target)
    renumber(links)
    save(ARCHIVE_PATH, archive)
    save(LINKS_PATH, data)
    print(f"archived: {args.id}")
    return 0


def cmd_reorder(args) -> int:
    data = load(LINKS_PATH)
    links = data.get("links", [])
    requested = [s.strip() for s in args.order.split(",") if s.strip()]
    by_id = {l["id"]: l for l in links}
    missing = [r for r in requested if r not in by_id]
    if missing:
        print(f"error: ids not found: {missing}", file=sys.stderr)
        return 2
    extras = [l["id"] for l in links if l["id"] not in requested]
    final_order = requested + extras
    for i, lid in enumerate(final_order, start=1):
        by_id[lid]["position"] = i
    save(LINKS_PATH, data)
    print(f"reordered: {final_order}")
    return 0


def cmd_move(args) -> int:
    return cmd_edit(argparse.Namespace(
        id=args.id, title=None, url=None, icon=None, tags=None, position=args.to,
    ))


def main() -> int:
    p = argparse.ArgumentParser(description="Edit data/links.json")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List current links").set_defaults(func=cmd_list)

    a = sub.add_parser("add", help="Add a new link")
    a.add_argument("--title", required=True)
    a.add_argument("--url", required=True)
    a.add_argument("--id", help="Stable slug (default: derived from title)")
    a.add_argument("--icon", default=None)
    a.add_argument("--tags", default=None, help="Comma-separated tags")
    a.add_argument("--position", type=int, default=None)
    a.add_argument("--click-estimate", type=int, default=None, dest="click_estimate")
    a.set_defaults(func=cmd_add)

    e = sub.add_parser("edit", help="Edit an existing link by id")
    e.add_argument("--id", required=True)
    e.add_argument("--title")
    e.add_argument("--url")
    e.add_argument("--icon")
    e.add_argument("--tags")
    e.add_argument("--position", type=int)
    e.set_defaults(func=cmd_edit)

    ar = sub.add_parser("archive", help="Move a link to data/archive.json")
    ar.add_argument("--id", required=True)
    ar.add_argument("--reason")
    ar.set_defaults(func=cmd_archive)

    r = sub.add_parser("reorder", help="Set order via comma-separated id list")
    r.add_argument("--order", required=True)
    r.set_defaults(func=cmd_reorder)

    m = sub.add_parser("move", help="Move a link to a specific position")
    m.add_argument("--id", required=True)
    m.add_argument("--to", type=int, required=True)
    m.set_defaults(func=cmd_move)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
