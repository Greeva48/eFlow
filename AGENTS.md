# AGENTS.md - eFlow

eFlow is the visual programming and dataflow authoring component for
EmbeddedOS, layered on EoStudio and eBuild. Its status is Prototype: the default
branch contains a host-side Python implementation that validates flow documents
and simulates them tick by tick, with a pytest suite and CI. Target code
generation and the EoStudio visual editors do not exist yet. (Provenance:
`README.md` and the inspected `master` tree.)

## Repository layout

- `README.md` - project purpose, status, ownership, and architecture links.
- `LICENSE` - MIT license.
- `eflow/interpreter.py` - flow loading, validation, the node registry (six
  node types; the `sensor.tmp117` node is simulated), and the tick-by-tick
  runner.
- `eflow/cli.py`, `eflow/__main__.py` - `python -m eflow validate <flow.json>`
  and `python -m eflow run <flow.json>`.
- `eflow/mcp_server.py`, `eflow/mcp_tools.py` - stdio MCP server exposing the
  `eflow_validate` tool (`python -m eflow.mcp_server`).
- `eflow/flows/` - example flows.
- `schema/eflow-flow.schema.json` - JSON Schema for flow documents.
- `llms.txt`, `llms-full.txt` - short and full plain-text summaries of the
  repository.
- `server.json` - MCP registry manifest; its version must match `__version__`
  in `eflow/__init__.py`.
- `skills/eflow-validate/` - the `eflow-validate` skill and its flow-format
  reference.
- `tests/` - pytest suite.
- `docs/dataflow-design.md`, `docs/review-note-2026-10-07.md` - design notes.
- `docs/wiki/` - source-controlled copies of the six published GitHub Wiki
  pages. They predate the prototype and still describe a documentation-only
  repository.
- `.github/workflows/ci.yml` - pytest on Python 3.10, 3.11, and 3.12, and a
  smoke run of the two example flows.
- `.github/workflows/server-json.yml` - `server.json` validation.
- `.github/workflows/linked-issue.yml` - organization linked-issue policy caller.
- `.github/PULL_REQUEST_TEMPLATE.md` - repository pull request checklist.

## Development

Read `README.md` before proposing product work. The package uses only the
Python standard library at runtime; CI tests it on Python 3.10, 3.11, and
3.12, and the tests need `pytest`. There is no package manifest yet, so run
everything from a checkout. Do not invent project commands or introduce a
second runtime. Do not describe target code generation or visual editing as
available until they exist in this repository.

## Validation

These are the commands CI runs, plus the CLI validator:

```bash
pip install pytest
python -m pytest tests/ -v --tb=short
python -m eflow.interpreter eflow/flows/temp_monitor.json --ticks 5
python -m eflow.interpreter eflow/flows/fan_control.json --ticks 5
python -m eflow validate eflow/flows/temp_monitor.json
git diff --check
```

For documentation-only changes, `git diff --check` and a Markdown lint of the
changed files are enough; say which checks you ran.

## Pull requests

Open a same-repository issue before opening a human-authored pull request. In the
pull request body, replace the template placeholder with a GitHub closing keyword
and that issue number, for example `Fixes #3`. Keep changes focused and explain
validation results and any pre-existing baseline blockers.

## Security

Do not report suspected vulnerabilities in a public issue. The current default
branch has no root `SECURITY.md`; use GitHub's private security advisory workflow
when available, or a private maintainer contact exposed by the organization.
