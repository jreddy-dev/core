from fastapi import APIRouter
from ..db import SessionLocal
from ..models import Video
from ..models_extra import ProtocolVersion
import json

router = APIRouter(prefix="/labels", tags=["labels"])


@router.post("/correction")
def post_correction(payload: dict):
    # payload expected: {video_id, experiment_id, corrected_protocol (json), user}
    session = SessionLocal()
    # store corrected protocol as a ProtocolVersion as well
    pv = ProtocolVersion(experiment_id=payload.get('experiment_id'), content_markdown=payload.get('corrected_markdown', ''), generated_by_video_id=payload.get('video_id'))
    session.add(pv)

    # store raw correction for retraining
    from ..models_extra import LabeledCorrection
    lc = LabeledCorrection(video_id=payload.get('video_id'), experiment_id=payload.get('experiment_id'), user_id=payload.get('user'), corrected_json=payload.get('corrected_protocol'), notes=payload.get('notes', ''))
    session.add(lc)

    session.commit()
    session.refresh(pv)
    session.refresh(lc)
    session.close()
    return {"protocol_version_id": pv.id, "correction_id": lc.id}


@router.get('/corrections')
def list_corrections(video_id: str = None):
    session = SessionLocal()
    q = session.query(LabeledCorrection)
    if video_id:
        q = q.filter(LabeledCorrection.video_id == video_id)
    items = q.all()
    session.close()
    return [{"id": i.id, "video_id": i.video_id, "experiment_id": i.experiment_id, "created_at": getattr(i, 'created_at', None)} for i in items]
