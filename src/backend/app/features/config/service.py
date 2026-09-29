from pathlib import Path
DEFAULT = {"rules": {"no_todo": True, "no_secret_like": True, "trailing_space": True}}
def load_rules(root: Path) -> dict:
    path = root / ".devkit.yml"
    if not path.exists():
        return DEFAULT["rules"]
    try:
        import yaml
        data = yaml.safe_load(path.read_text()) or {}
        return DEFAULT["rules"] | (data.get("rules") or {})
    except Exception:
        return DEFAULT["rules"]
