from pathlib import Path
def apply_safe(root: str, findings: list[dict]) -> int:
    changed = 0
    by_file = {}
    for f in findings:
        if f.get("rule") == "trailing_space" and f.get("fixable"):
            by_file.setdefault(f["path"], []).append(f["line"])
    base = Path(root)
    for rel, lines in by_file.items():
        path = base / rel
        text = path.read_text(errors="ignore").splitlines()
        for n in lines:
            if 1 <= n <= len(text):
                text[n - 1] = text[n - 1].rstrip()
        path.write_text("\n".join(text) + "\n")
        changed += 1
    return changed
