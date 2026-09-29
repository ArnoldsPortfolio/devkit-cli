import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.scan.engine import scan_repo
from app.kernel.ids import new_id
from app.models import ScanRow
class ScanStore:
    def __init__(self, db: Session):
        self.db = db
    def run(self, owner_id: str, root: str) -> dict:
        report = scan_repo(root)
        row = ScanRow(id=new_id(), owner_id=owner_id, root=report["root"], finding_count=len(report["findings"]), exit_code=report["exit_code"], report=json.dumps(report))
        self.db.add(row); self.db.commit()
        return _out(row)
    def list(self, owner_id: str) -> list[dict]:
        return [_out(r) for r in self.db.scalars(select(ScanRow).where(ScanRow.owner_id == owner_id))]
    def get(self, owner_id: str, scan_id: str) -> dict:
        row = self.db.get(ScanRow, scan_id)
        return _out(row) if row and row.owner_id == owner_id else {"findings": []}
def _out(row: ScanRow) -> dict:
    body = json.loads(row.report)
    return {"id": row.id, "root": row.root, "finding_count": row.finding_count, "exit_code": row.exit_code, "findings": body.get("findings", [])}
