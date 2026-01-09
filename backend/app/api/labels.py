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
    session.commit()
    session.refresh(pv)
    session.close()
    return {"id": pv.id}
