from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from ..db import SessionLocal
from ..models import Video

router = APIRouter(prefix="/videos", tags=["videos"])

VIDEO_DIR = os.getenv("VIDEO_DIR", "/data/videos")
os.makedirs(VIDEO_DIR, exist_ok=True)


@router.post("/{experiment_id}")
async def upload_video(experiment_id: str, file: UploadFile = File(...)):
    # Save file
    video_id = str(uuid4())
    filename = f"{video_id}_{file.filename}"
    path = os.path.join(VIDEO_DIR, filename)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)

    session = SessionLocal()
    v = Video(id=video_id, experiment_id=experiment_id, filename=filename, url=path, status="uploaded")
    session.add(v)
    session.commit()
    session.refresh(v)
    session.close()

    return JSONResponse(status_code=201, content={"id": video_id, "filename": filename, "status": "uploaded"})


@router.get("/{video_id}")
def get_video(video_id: str):
    session = SessionLocal()
    v = session.query(Video).filter(Video.id == video_id).first()
    session.close()
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"id": v.id, "filename": v.filename, "status": v.status, "url": v.url}
