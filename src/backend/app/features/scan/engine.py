import re
from pathlib import Path
from app.features.config.service import load_rules
SKIP = {".git", "node_modules", ".venv", "__pycache__", ".next"}
TEXT = {".py", ".ts", ".tsx", ".js", ".md", ".yml", ".yaml", ".json"}
TODO = re.compile(r"\b(TODO|FIXME)\b")
SECRET = re.compile(r"(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]+['\"]", re.I)
def scan_repo(root: str) -> dict:
    base = Path(root).resolve()
    rules = load_rules(base)
    findings = []
    for path in _files(base):
        findings.extend(_analyze(base, path, rules))
    return {"root": str(base), "findings": findings, "exit_code": 1 if findings else 0}
def _files(base: Path):
    for path in base.rglob("*"):
        if path.is_file() and path.suffix in TEXT and SKIP.isdisjoint(path.parts):
            yield path
def _analyze(base: Path, path: Path, rules: dict) -> list[dict]:
    try:
        lines = path.read_text(errors="ignore").splitlines()
    except Exception:
        return []
    rel = str(path.relative_to(base))
    hits = []
    for i, line in enumerate(lines, 1):
        if rules.get("no_todo") and TODO.search(line):
            hits.append(_finding(rel, i, "no_todo", line.strip(), False))
        if rules.get("no_secret_like") and SECRET.search(line):
            hits.append(_finding(rel, i, "no_secret_like", line.strip(), False))
        if rules.get("trailing_space") and line.rstrip() != line:
            hits.append(_finding(rel, i, "trailing_space", line.rstrip() + "·", True))
    return hits
def _finding(path: str, line: int, rule: str, snippet: str, fixable: bool) -> dict:
    return {"path": path, "line": line, "rule": rule, "snippet": snippet[:160], "fixable": fixable}
