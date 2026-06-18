#!/usr/bin/env python3
"""Example stdlib kernel — STUB. Shows the idioms; contains no real API logic.

Demonstrates, for a real plugin to copy:
  - stdlib-only HTTP (urllib) + JSON, no third-party deps, no server
  - secrets/token loaded from OUTSIDE the repo (XDG path, 0600) — never committed
  - agent-legible output shaping: concise vs detailed, human-readable fields, pagination
  - actionable error messages (steer the agent), never raw tracebacks

Replace the stub `list` command with real operations. Keep the shaping patterns.
"""
import argparse
import json
import os
import sys
from pathlib import Path

# --- Secrets live OUTSIDE the repo. Never write tokens into the project tree. ---
# XDG state dir, e.g. ~/.local/state/<plugin>/token.json, created 0700/0600 by the auth flow.
APP = "example"  # rename per plugin
STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / APP
TOKEN_PATH = STATE_DIR / "token.json"


def load_token() -> dict:
    """Load the cached token from the XDG path. Returns {} if absent."""
    if not TOKEN_PATH.exists():
        return {}
    return json.loads(TOKEN_PATH.read_text())


# --- stdlib HTTP idiom (shown, not used by the stub) -------------------------
def _api_get(url: str, token: str) -> dict:
    """Example of the only HTTP primitive a plugin needs — urllib, no SDK.

    import urllib.request
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:   # noqa: S310 (trusted host)
        return json.load(r)
    """
    raise NotImplementedError("stub — implement with urllib.request in a real plugin")


# --- agent-legible output shaping --------------------------------------------
def _render(items: list[dict], fmt: str) -> str:
    """concise = human-readable summary; detailed = adds IDs for follow-up calls."""
    if fmt == "detailed":
        return json.dumps(items, indent=2)
    lines = [f'- "{it["title"]}" from {it["sender"]}  (folder: {it["folder"]})' for it in items]
    lines.append(f"{len(items)} items. Pass --format detailed for IDs needed by follow-up commands.")
    return "\n".join(lines)


def cmd_list(args) -> int:
    if not load_token():
        # actionable error, not a traceback
        print(f"error: not signed in — run /{APP}-auth-login first, then retry.", file=sys.stderr)
        return 1
    # STUB data — a real command would page the API with args.limit and resolve IDs to names here.
    items = [
        {"id": "AAStub1", "title": "Weekly Newsletter", "sender": "news@example.com", "folder": "Inbox"},
        {"id": "AAStub2", "title": "Receipt #4471", "sender": "billing@example.com", "folder": "Inbox"},
    ][: args.limit]
    print(_render(items, args.format))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog=APP, description="Example stdlib plugin kernel (stub).")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_list = sub.add_parser("list", help="example read-only listing (stub)")
    p_list.add_argument("--limit", type=int, default=25, help="max items (pagination default)")
    p_list.add_argument("--format", choices=["concise", "detailed"], default="concise")
    p_list.set_defaults(func=cmd_list)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
