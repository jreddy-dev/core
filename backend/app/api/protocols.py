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


@router.post("/experiment/{experiment_id}")
def create_protocol(experiment_id: str, payload: dict):
    session = SessionLocal()
    pv = ProtocolVersion(experiment_id=experiment_id, content_markdown=payload.get('content_markdown', ''), generated_by_video_id=payload.get('generated_by_video_id', None), confidence_score=payload.get('confidence_score', None))
    session.add(pv)
    session.commit()
    session.refresh(pv)
    session.close()
    return {"id": pv.id, "content_markdown": pv.content_markdown, "created": getattr(pv, 'created_at', None)}
