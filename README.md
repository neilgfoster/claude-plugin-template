# claude-plugin-template

A minimal skeleton for a Claude Code plugin. Stdlib-only, zero-dependency,
zero-backend by convention. Copy it to start a new plugin with a consistent layout and the
agent-friendly conventions already in place.

This is **layout only — no framework, no shared abstractions.** Real reusable abstractions get
harvested later, from working plugins, not invented up front.

## Layout

Two tiers: the **repo root** builds/tests/distributes the plugin; **`plugin/`** is the shippable
payload that gets installed.

```
.claude-plugin/marketplace.json   # marketplace manifest — points at ./plugin ({{NAME}} placeholder)
plugin/                           # THE PLUGIN PAYLOAD (this is what installs)
  .claude-plugin/plugin.json      #   plugin manifest ({{NAME}}/{{DESCRIPTION}} placeholders)
  skills/<subject>-<verb>/SKILL.md#   one exemplary skill demonstrating the conventions
  src/<plugin>/                   #   stdlib Python kernel (importable + runnable by skills)
    client.py                     #     urllib+json idiom + output-shaping patterns (stub)
  hooks/hooks.json                #   optional PreToolUse example (delete if unused)
pyproject.toml                    # ruff + pytest config (dev tooling only — never ships)
tests/                            # guards the manifest install path + the runnable kernel
.github/workflows/{ci,release}.yml# lint+test on PR; tag-driven GitHub Release
CHANGELOG.md  CONTRIBUTING.md      # Keep-a-Changelog + contributor standards
docs/AGENT-FRIENDLY.md            # REQUIRED READING before adding a skill
```

Inside the plugin, reference bundled files via `${CLAUDE_PLUGIN_ROOT}/...` — it resolves to `plugin/`.

## How to instantiate

1. Copy this repo to `~/source/neilgfoster/<plugin>` and `git init`.
2. Rename `plugin/src/example` → `plugin/src/<plugin>`; update `APP` in `client.py` and
   `known-first-party` in `pyproject.toml`.
3. Rename `plugin/skills/example-subject-verb` → real `<subject>-<verb>` skills.
4. Fill the `{{NAME}}` / `{{DESCRIPTION}}` placeholders in `.claude-plugin/marketplace.json` and
   `plugin/.claude-plugin/plugin.json` (the marketplace entry name must equal the plugin name).
5. Build features spec-first (Spec-Driven Development):
   `/speckit-specify` → `clarify` → `plan` → `tasks` → `implement`.

## Verify before done

`ruff` and `pytest` are dev tooling only — they never ship inside `plugin/`. If `python3 -m pip`
is unavailable, install them isolated with [`uv`](https://docs.astral.sh/uv/)
(`uv tool install ruff pytest`, then `export PATH="$HOME/.local/bin:$PATH"`).

```sh
ruff check . && ruff format --check .   # apply with `ruff format .` if it wants changes
python3 -m pytest -q

# Stdlib-only guard — the same grep CI enforces in tests/test_stdlib_only.py. The shipped
# payload under plugin/src must import only the standard library (plus its own package).
grep -rnE '^\s*(import|from)\s+(msal|azure|requests|urllib3|httpx|aiohttp|msgraph|pydantic|yaml|dotenv)\b' plugin/src && echo 'FORBIDDEN IMPORT' || echo 'stdlib-only OK'
```

## Non-negotiable conventions

- **stdlib only, zero dependencies, no backend.** `urllib` for HTTP, `json` for parsing.
- **Secrets/tokens live OUTSIDE the repo** — a user-level XDG path
  (`${XDG_STATE_HOME:-~/.local/state}/<plugin>/`) with `0600` perms. Never committed, not even
  encrypted. This repo must not depend on git-crypt.
- **Agent-friendly by design** — every skill follows `docs/AGENT-FRIENDLY.md` (MCP/agent-tool
  principles: onboarding descriptions, behavioural annotations, flat JSON-schema inputs, agent-legible
  output, steering errors).
