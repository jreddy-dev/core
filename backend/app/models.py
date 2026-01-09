from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .db import Base
import uuid


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=gen_uuid)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)


class Node(Base):
    __tablename__ = "nodes"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    metadata = Column(JSON, default={})


class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(String, primary_key=True, default=gen_uuid)
    node_id = Column(String, ForeignKey("nodes.id"), unique=True)
    title = Column(String)
    description = Column(String)


class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True, default=gen_uuid)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    filename = Column(String)
    url = Column(String)
    status = Column(String, default="uploaded")


class ProcessingResult(Base):
    __tablename__ = "processing_results"
    id = Column(String, primary_key=True, default=gen_uuid)
    video_id = Column(String, ForeignKey("videos.id"))
    transcripts = Column(JSON)
    detections = Column(JSON)
    actions = Column(JSON)
    ocr = Column(JSON)
    summary_text = Column(String)
