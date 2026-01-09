from fastapi import FastAPI
from .api import experiments, videos, projects, protocols
from .db import Base, engine
import models_extra

app = FastAPI(title="LabFlow Prototype")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(experiments.router, prefix="/api")
app.include_router(videos.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(protocols.router, prefix="/api")
from .api import downloads
app.include_router(downloads.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
