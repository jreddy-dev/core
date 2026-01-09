from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import os
from ..db import SessionLocal
from ..models import Video

router = APIRouter(prefix="/downloads", tags=["downloads"])


@router.get("/{video_id}")
def download_video(video_id: str):
    session = SessionLocal()
    v = session.query(Video).filter(Video.id == video_id).first()
    session.close()
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    path = v.url
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile():
        with open(path, 'rb') as f:
            data = f.read()
            if v.encrypted:
                try:
                    from cryptography.fernet import Fernet
                    key = os.getenv('ENCRYPTION_KEY').encode()
                    fernet = Fernet(key)
                    data = fernet.decrypt(data)
                except Exception:
                    raise HTTPException(status_code=500, detail='Decrypt failed')
            yield data

    return StreamingResponse(iterfile(), media_type='application/octet-stream')
