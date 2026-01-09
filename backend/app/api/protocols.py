from fastapi import APIRouter, HTTPException
from ..db import SessionLocal
from ..models_extra import ProtocolVersion

router = APIRouter(prefix="/protocols", tags=["protocols"])


@router.get("/experiment/{experiment_id}")
def get_protocols(experiment_id: str):
    session = SessionLocal()
    pvs = session.query(ProtocolVersion).filter(ProtocolVersion.experiment_id == experiment_id).all()
    session.close()
    return [{"id": p.id, "content_markdown": p.content_markdown, "created": getattr(p, 'created_at', None)} for p in pvs]
