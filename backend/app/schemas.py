from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID


class VideoCreate(BaseModel):
    filename: str


class Video(BaseModel):
    id: str
    experiment_id: Optional[str]
    filename: str
    url: Optional[str]
    status: str

    class Config:
        orm_mode = True


class Experiment(BaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
