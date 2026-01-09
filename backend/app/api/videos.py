from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from ..db import SessionLocal
from ..models import Video

router = APIRouter(prefix="/videos", tags=["videos"])

VIDEO_DIR = os.getenv("VIDEO_DIR", "/data/videos")
os.makedirs(VIDEO_DIR, exist_ok=True)


@router.post("/{experiment_id}")
async def upload_video(experiment_id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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

    # enqueue background processing automatically
    background_tasks.add_task(process_video_task, video_id)

    return JSONResponse(status_code=201, content={"id": video_id, "filename": filename, "status": "uploaded"})


@router.post("/{video_id}/process")
def process_video_endpoint(video_id: str, background_tasks: BackgroundTasks):
    # Enqueue background processing
    background_tasks.add_task(process_video_task, video_id)
    return JSONResponse(status_code=202, content={"video_id": video_id, "status": "processing"})


def process_video_task(video_id: str):
    try:
        from ..workers.process_video import process_video
        process_video(video_id)
    except Exception as e:
        print("Processing error:", e)


@router.post("/{video_id}/synthesize")
def synthesize(video_id: str):
    try:
        from ..workers.process_video import synthesize_protocol
        md = synthesize_protocol(video_id)
        return JSONResponse(status_code=200, content={"protocol_markdown": md})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}")
def get_video(video_id: str):
    session = SessionLocal()
    v = session.query(Video).filter(Video.id == video_id).first()
    session.close()
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"id": v.id, "filename": v.filename, "status": v.status, "url": v.url}
