from fastapi import FastAPI
from .api import experiments, videos
from .db import Base, engine

app = FastAPI(title="LabFlow Prototype")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(experiments.router, prefix="/api")
app.include_router(videos.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
