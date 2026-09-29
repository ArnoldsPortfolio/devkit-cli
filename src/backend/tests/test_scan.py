from pathlib import Path
from app.cli import main
from app.features.scan.engine import scan_repo

def test_scan_finds_todo(tmp_path: Path):
    marker = "TO" + "DO"
    (tmp_path / "demo.py").write_text(f"x = 1  \n# {marker} ship this\n")
    report = scan_repo(str(tmp_path))
    rules = {f["rule"] for f in report["findings"]}
    assert "no_todo" in rules
    assert "trailing_space" in rules
    assert report["exit_code"] == 1

def test_cli_exit_codes(tmp_path: Path):
    (tmp_path / "clean.py").write_text("print(1)\n")
    assert main(["scan", str(tmp_path)]) == 0
