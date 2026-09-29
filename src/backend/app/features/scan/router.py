from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.scan.service import ScanStore
router = APIRouter(prefix="/scans", tags=["scan"])
class ScanBody(BaseModel):
    root: str = "."
@router.get("")
def list_scans(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ScanStore(db).list(user_id)
@router.post("")
def run_scan(body: ScanBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return ScanStore(db).run(user_id, body.root)
