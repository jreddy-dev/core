from fastapi import APIRouter, HTTPException
from ..db import SessionLocal
from ..models import Node, Project
from typing import List
from ..schemas import Experiment as ExperimentSchema
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    title: str
    description: str = ""


@router.post("/", response_model=dict)
def create_project(payload: ProjectCreate):
    session = SessionLocal()
    p = Project(title=payload.title, description=payload.description, owner_id="demo")
    session.add(p)
    session.commit()
    session.refresh(p)
    session.close()
    return {"id": p.id, "title": p.title}


@router.get("/{project_id}/nodes")
def get_nodes(project_id: str):
    session = SessionLocal()
    nodes = session.query(Node).filter(Node.project_id == project_id).all()
    session.close()
    return [{"id": n.id, "type": n.type, "title": n.title, "metadata": n.metadata} for n in nodes]


@router.post("/{project_id}/nodes")
def create_node(project_id: str, payload: dict):
    session = SessionLocal()
    node = Node(project_id=project_id, type=payload.get("type", "experiment"), title=payload.get("title", "Untitled"), metadata=payload.get("metadata", {}))
    session.add(node)
    session.commit()
    session.refresh(node)
    session.close()
    return {"id": node.id, "type": node.type, "title": node.title}
