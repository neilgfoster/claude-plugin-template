<!--
PR title should be a Conventional Commit (e.g. `feat: ...`, `fix: ...`, `docs: ...`).
Keep it minimal — this is a template repo. Delete sections that genuinely don't apply.
-->

## What and why

<!-- One paragraph: what this changes and why. -->

## Conventions

- [ ] Runtime stays **stdlib-only, zero-dependency, zero-backend** (`urllib`/`json`; ruff/pytest are
  dev tooling only).
- [ ] No secrets/tokens in the repo — they live outside it in an XDG path (`0600`).
- [ ] Any new/changed skill follows `docs/AGENT-FRIENDLY.md` (description + CLI I/O are the contract).
- [ ] The template stays minimal — layout + exemplary patterns only, no speculative framework.

## Verification

```sh
ruff check . && ruff format --check .
python3 -m pytest -q
```

- [ ] `ruff check .` and `ruff format --check .` pass.
- [ ] `python3 -m pytest -q` passes.
