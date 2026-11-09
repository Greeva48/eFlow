"""Check AGENTS.md against the eFlow tree it describes.

Usage (from the repo root): python -I check_agents_md.py
1. Statements that say there is no code or no tests, checked against the tree.
2. Every path named in the "Repository layout" list must exist.
3. Every `python -m ...` command in the bash block must exit 0.
Exit status 1 if anything fails.
"""

import pathlib
import re
import subprocess
import sys

root = pathlib.Path.cwd()
text = (root / "AGENTS.md").read_text(encoding="utf-8")
flat = " ".join(text.split())
fails = 0


def report(ok, what):
    global fails
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {what}")


has_code = any((root / "eflow").glob("*.py"))
n_tests = len(list((root / "tests").glob("test_*.py")))
print(f"# tree: eflow/*.py present={has_code}, tests/test_*.py files={n_tests}")
for claim in [
    "only project documentation and a license",
    "there is no implementation",
    "does not yet contain a runtime, package manifest, build system, test suite",
    "There is no repository-native build or test command",
]:
    present = claim.lower() in flat.lower()
    report(not present, f'no stale claim: "{claim}"' + ("  <- says this, but the tree has code and tests" if present else ""))

layout = text.split("## Repository layout", 1)[1].split("\n## ", 1)[0]
for item in re.split(r"\n- ", layout):
    head = item.split(" - ", 1)[0]
    for p in re.findall(r"`([A-Za-z0-9_.\-/]+)`", head):
        report((root / p).exists(), f"layout path exists: {p}")

block = re.search(r"```bash\n(.*?)```", text, re.S)
cmds = [c.strip() for c in (block.group(1).splitlines() if block else []) if c.strip().startswith("python -m")]
report(bool(cmds), f"validation block lists {len(cmds)} python command(s)")
for c in cmds:
    r = subprocess.run(c.split(), cwd=root, capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or [""])[-1][:90]
    report(r.returncode == 0, f"runs: {c}  -> exit {r.returncode}  {tail}")

print(f"# {fails} failed")
sys.exit(1 if fails else 0)
