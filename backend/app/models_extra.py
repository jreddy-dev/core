from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, func
from sqlalchemy.orm import relationship
from .db import Base
import uuid


def gen_uuid():
    return str(uuid.uuid4())


class ProtocolVersion(Base):
    __tablename__ = "protocol_versions"
    id = Column(String, primary_key=True, default=gen_uuid)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    editor_id = Column(String, ForeignKey("users.id"), nullable=True)
    content_markdown = Column(String)
    generated_by_video_id = Column(String, ForeignKey("videos.id"), nullable=True)
    confidence_score = Column(Integer)


class Reagent(Base):
    __tablename__ = "reagents"
    id = Column(String, primary_key=True, default=gen_uuid)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    name = Column(String)
    catalog_number = Column(String)
    concentration = Column(String)
    supplier = Column(String)


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(String, primary_key=True, default=gen_uuid)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    name = Column(String)
    model = Column(String)


class Step(Base):
    __tablename__ = "steps"
    id = Column(String, primary_key=True, default=gen_uuid)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    start_ts = Column(String)
    end_ts = Column(String)
    action_label = Column(String)
    description = Column(String)
    objects = Column(JSON)
    confidence = Column(Integer)


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=gen_uuid)
    owner_id = Column(String, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String)


class Link(Base):
    __tablename__ = "links"
    id = Column(String, primary_key=True, default=gen_uuid)
    from_node_id = Column(String, ForeignKey("nodes.id"))
    to_node_id = Column(String, ForeignKey("nodes.id"))
