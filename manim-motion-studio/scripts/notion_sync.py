#!/usr/bin/env python3
"""
Notion API sync helper for Manim Motion Studio video production workflows.
Works with `notion-client` if installed, or falls back to pure-stdlib `urllib`.

Requires environment variable: NOTION_TOKEN
Subcommands: search, read-page, query-db, create-page, update-status, append, comment, log-render
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def _token() -> str:
    tok = os.environ.get("NOTION_TOKEN", "").strip()
    if not tok:
        raise RuntimeError(
            "NOTION_TOKEN environment variable is not set. "
            "Export your Notion integration secret or use the connected Notion app."
        )
    return tok


def _api_request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{NOTION_API_BASE}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method.upper(),
        headers={
            "Authorization": f"Bearer {_token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API {method} {path} failed ({exc.code}): {body}") from exc


def _rich_text_plain(items: list[dict[str, Any]] | None) -> str:
    if not items:
        return ""
    return "".join(part.get("plain_text", "") for part in items)


def _extract_title(obj: dict[str, Any]) -> str:
    if obj.get("object") == "database":
        return _rich_text_plain(obj.get("title")) or "(Untitled Database)"
    props = obj.get("properties", {})
    for prop in props.values():
        if prop.get("type") == "title":
            return _rich_text_plain(prop.get("title")) or "(Untitled Page)"
    return "(Untitled)"


def _flatten_property(prop: dict[str, Any]) -> Any:
    ptype = prop.get("type")
    if ptype == "title":
        return _rich_text_plain(prop.get("title"))
    if ptype == "rich_text":
        return _rich_text_plain(prop.get("rich_text"))
    if ptype == "number":
        return prop.get("number")
    if ptype == "select":
        sel = prop.get("select")
        return sel.get("name") if sel else None
    if ptype == "status":
        st = prop.get("status")
        return st.get("name") if st else None
    if ptype == "multi_select":
        return [x.get("name") for x in prop.get("multi_select", [])]
    if ptype == "checkbox":
        return prop.get("checkbox")
    if ptype == "date":
        d = prop.get("date")
        return d.get("start") if d else None
    if ptype == "url":
        return prop.get("url")
    if ptype == "email":
        return prop.get("email")
    if ptype == "relation":
        return [r.get("id") for r in prop.get("relation", [])]
    if ptype == "formula":
        f = prop.get("formula", {})
        return f.get(f.get("type"))
    return None


def _block_to_markdown(block: dict[str, Any]) -> str:
    btype = block.get("type", "")
    data = block.get(btype, {})
    txt = _rich_text_plain(data.get("rich_text"))
    if btype == "heading_1":
        return f"# {txt}"
    if btype == "heading_2":
        return f"## {txt}"
    if btype == "heading_3":
        return f"### {txt}"
    if btype == "bulleted_list_item":
        return f"- {txt}"
    if btype == "numbered_list_item":
        return f"1. {txt}"
    if btype == "to_do":
        mark = "x" if data.get("checked") else " "
        return f"- [{mark}] {txt}"
    if btype == "quote":
        return f"> {txt}"
    if btype == "callout":
        return f"> [Callout] {txt}"
    if btype == "code":
        lang = data.get("language", "")
        return f"```{lang}\n{txt}\n```"
    if btype == "divider":
        return "---"
    return txt


def _make_blocks_from_text(text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("### "):
            btype, content = "heading_3", line[4:]
        elif line.startswith("## "):
            btype, content = "heading_2", line[3:]
        elif line.startswith("# "):
            btype, content = "heading_1", line[2:]
        elif line.startswith("- [ ] "):
            blocks.append(
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "checked": False,
                        "rich_text": [{"type": "text", "text": {"content": line[6:][:1900]}}],
                    },
                }
            )
            continue
        elif line.startswith("- [x] ") or line.startswith("- [X] "):
            blocks.append(
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "checked": True,
                        "rich_text": [{"type": "text", "text": {"content": line[6:][:1900]}}],
                    },
                }
            )
            continue
        elif line.startswith("- "):
            btype, content = "bulleted_list_item", line[2:]
        else:
            btype, content = "paragraph", line
        blocks.append(
            {
                "object": "block",
                "type": btype,
                btype: {"rich_text": [{"type": "text", "text": {"content": content[:1900]}}]},
            }
        )
    return blocks


def cmd_search(args: argparse.Namespace) -> None:
    payload: dict[str, Any] = {"page_size": args.limit}
    if args.query:
        payload["query"] = args.query
    res = _api_request("POST", "/search", payload)
    rows = []
    for item in res.get("results", []):
        rows.append(
            {
                "id": item.get("id"),
                "object": item.get("object"),
                "title": _extract_title(item),
                "url": item.get("url"),
                "last_edited_time": item.get("last_edited_time"),
            }
        )
    print(json.dumps(rows, indent=2))


def cmd_read_page(args: argparse.Namespace) -> None:
    page = _api_request("GET", f"/pages/{args.page_id}")
    lines = [f"# {_extract_title(page)}", ""]
    cursor: str | None = None
    while True:
        qs = f"?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        res = _api_request("GET", f"/blocks/{args.page_id}/children{qs}")
        for blk in res.get("results", []):
            md = _block_to_markdown(blk)
            if md:
                lines.append(md)
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
    text = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Saved page markdown to {args.out}")
    else:
        print(text)


def cmd_query_db(args: argparse.Namespace) -> None:
    rows: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        payload: dict[str, Any] = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        res = _api_request("POST", f"/databases/{args.database_id}/query", payload)
        for item in res.get("results", []):
            flat = {k: _flatten_property(v) for k, v in item.get("properties", {}).items()}
            flat["_id"] = item.get("id")
            flat["_url"] = item.get("url")
            rows.append(flat)
        if not res.get("has_more") or len(rows) >= args.limit:
            break
        cursor = res.get("next_cursor")
    rows = rows[: args.limit]
    text = json.dumps(rows, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Exported {len(rows)} database rows to {args.out}")
    else:
        print(text)


def cmd_create_page(args: argparse.Namespace) -> None:
    body_text = args.body or ""
    if args.body_file:
        body_text = Path(args.body_file).read_text(encoding="utf-8")

    if args.parent_db:
        parent = {"database_id": args.parent_db}
        title_prop = args.title_prop or "Name"
        properties: dict[str, Any] = {
            title_prop: {"title": [{"type": "text", "text": {"content": args.title}}]}
        }
        if args.status:
            properties[args.status_prop] = (
                {"status": {"name": args.status}}
                if args.prop_type == "status"
                else {"select": {"name": args.status}}
            )
    elif args.parent_page:
        parent = {"page_id": args.parent_page}
        properties = {"title": {"title": [{"type": "text", "text": {"content": args.title}}]}}
    else:
        raise RuntimeError("Provide either --parent-db or --parent-page.")

    payload: dict[str, Any] = {"parent": parent, "properties": properties}
    if body_text.strip():
        payload["children"] = _make_blocks_from_text(body_text)[:100]

    res = _api_request("POST", "/pages", payload)
    print(json.dumps({"id": res.get("id"), "url": res.get("url")}, indent=2))


def cmd_update_status(args: argparse.Namespace) -> None:
    prop_payload = (
        {"status": {"name": args.value}}
        if args.prop_type == "status"
        else {"select": {"name": args.value}}
        if args.prop_type == "select"
        else {"rich_text": [{"type": "text", "text": {"content": args.value}}]}
    )
    res = _api_request("PATCH", f"/pages/{args.page_id}", {"properties": {args.prop: prop_payload}})
    print(json.dumps({"id": res.get("id"), "url": res.get("url"), "updated": args.prop}, indent=2))


def cmd_append(args: argparse.Namespace) -> None:
    text = Path(args.file).read_text(encoding="utf-8") if args.file else (args.text or "")
    blocks = _make_blocks_from_text(text)
    if not blocks:
        raise RuntimeError("Nothing to append.")
    for idx in range(0, len(blocks), 100):
        _api_request("PATCH", f"/blocks/{args.page_id}/children", {"children": blocks[idx : idx + 100]})
    print(f"Appended {len(blocks)} block(s) to {args.page_id}")


def cmd_comment(args: argparse.Namespace) -> None:
    res = _api_request(
        "POST",
        "/comments",
        {
            "parent": {"page_id": args.page_id},
            "rich_text": [{"type": "text", "text": {"content": args.text[:1900]}}],
        },
    )
    print(json.dumps({"comment_id": res.get("id")}, indent=2))


def cmd_log_render(args: argparse.Namespace) -> None:
    import re
    import shutil

    vpath = Path(args.video)
    if not vpath.exists():
        raise FileNotFoundError(f"Video not found: {vpath}")
    info_line = f"- Video: `{vpath.name}` ({vpath.stat().st_size / (1024 * 1024):.2f} MB)"
    try:
        ffmpeg_exe = shutil.which("ffmpeg")
        if not ffmpeg_exe:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        proc = subprocess.run([ffmpeg_exe, "-i", str(vpath)], capture_output=True, text=True)
        stderr = proc.stderr
        m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", stderr)
        m_res = re.search(r"Video:.*?,\s*(\d+)x(\d+)", stderr)
        m_fps = re.search(r"(\d+(?:\.\d+)?)\s*fps", stderr)
        if m_dur and m_res:
            dur = int(m_dur.group(1)) * 3600 + int(m_dur.group(2)) * 60 + float(m_dur.group(3))
            fps = m_fps.group(1) if m_fps else "?"
            info_line = (
                f"- Video: `{vpath.name}` | {m_res.group(1)}x{m_res.group(2)} "
                f"@ {fps} fps | {dur:.2f}s | {vpath.stat().st_size / (1024 * 1024):.2f} MB"
            )
    except Exception:
        pass

    lines = ["## Render Log", info_line]
    if args.notes:
        lines.append(f"- Notes: {args.notes}")
    blocks = _make_blocks_from_text("\n".join(lines))
    _api_request("PATCH", f"/blocks/{args.page_id}/children", {"children": blocks})
    print(f"Logged render metadata to Notion page {args.page_id}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Notion API sync helper for Manim Motion Studio.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search pages and databases")
    s.add_argument("query", nargs="?", default="", help="Search query")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_search)

    rp = sub.add_parser("read-page", help="Read a Notion page as Markdown")
    rp.add_argument("page_id")
    rp.add_argument("--out", help="Optional output .md file")
    rp.set_defaults(func=cmd_read_page)

    qd = sub.add_parser("query-db", help="Query a Notion database to JSON")
    qd.add_argument("database_id")
    qd.add_argument("--limit", type=int, default=100)
    qd.add_argument("--out", help="Optional output .json file")
    qd.set_defaults(func=cmd_query_db)

    cp = sub.add_parser("create-page", help="Create a Notion page in a database or parent page")
    cp.add_argument("--parent-db", help="Parent database ID")
    cp.add_argument("--parent-page", help="Parent page ID")
    cp.add_argument("--title", required=True)
    cp.add_argument("--title-prop", default="Name", help="Database title property name (default: Name)")
    cp.add_argument("--status", help="Initial status/select value")
    cp.add_argument("--status-prop", default="Status", help="Status property name (default: Status)")
    cp.add_argument("--prop-type", choices=["status", "select"], default="status")
    cp.add_argument("--body", help="Markdown/text body")
    cp.add_argument("--body-file", help="Path to Markdown/text file")
    cp.set_defaults(func=cmd_create_page)

    us = sub.add_parser("update-status", help="Update a page property (status/select/rich_text)")
    us.add_argument("page_id")
    us.add_argument("--prop", default="Status")
    us.add_argument("--value", required=True)
    us.add_argument("--prop-type", choices=["status", "select", "rich_text"], default="status")
    us.set_defaults(func=cmd_update_status)

    ap = sub.add_parser("append", help="Append text/Markdown blocks to a page")
    ap.add_argument("page_id")
    ap.add_argument("--text", help="Inline text/Markdown")
    ap.add_argument("--file", help="Path to Markdown/text file")
    ap.set_defaults(func=cmd_append)

    cm = sub.add_parser("comment", help="Add a comment to a Notion page")
    cm.add_argument("page_id")
    cm.add_argument("--text", required=True)
    cm.set_defaults(func=cmd_comment)

    lr = sub.add_parser("log-render", help="Log rendered MP4 metadata onto a Notion page")
    lr.add_argument("page_id")
    lr.add_argument("--video", required=True)
    lr.add_argument("--notes", default="")
    lr.set_defaults(func=cmd_log_render)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
