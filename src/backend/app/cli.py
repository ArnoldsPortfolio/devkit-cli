import argparse, sys
from app.features.fix.service import apply_safe
from app.features.report.service import as_json, pretty, sarif
from app.features.scan.engine import scan_repo
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="devkit")
    sub = parser.add_subparsers(dest="cmd", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("root", nargs="?", default=".")
    scan.add_argument("--format", choices=["pretty", "json", "sarif"], default="pretty")
    scan.add_argument("--fix", action="store_true")
    args = parser.parse_args(argv)
    report = scan_repo(args.root)
    if args.fix:
        apply_safe(report["root"], report["findings"])
        report = scan_repo(args.root)
    print({"pretty": pretty, "json": as_json, "sarif": sarif}[args.format](report))
    return report["exit_code"]
if __name__ == "__main__":
    raise SystemExit(main())
