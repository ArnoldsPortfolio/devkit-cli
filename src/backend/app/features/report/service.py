import json
def pretty(report: dict) -> str:
    lines = [f"{len(report['findings'])} finding(s) in {report['root']}"]
    for f in report["findings"]:
        lines.append(f"  {f['path']}:{f['line']}  {f['rule']}  {f['snippet']}")
    return "\n".join(lines)
def as_json(report: dict) -> str:
    return json.dumps(report, indent=2)
def sarif(report: dict) -> str:
    results = [{"ruleId": f["rule"], "level": "warning", "message": {"text": f["snippet"]}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": f["path"]}, "region": {"startLine": f["line"]}}}]} for f in report["findings"]]
    return json.dumps({"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "devkit"}}, "results": results}]})
