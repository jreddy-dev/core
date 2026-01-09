from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .. import db
from ..models import Experiment
from ..schemas import Experiment as ExperimentSchema

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("/", response_model=ExperimentSchema)
def create_experiment(payload: ExperimentSchema):
    session = db.SessionLocal()
    exp = Experiment(id=payload.id, title=payload.title, description=payload.description)
    session.add(exp)
    session.commit()
    session.refresh(exp)
    session.close()
    return exp


@router.get("/{id}", response_model=ExperimentSchema)
def get_experiment(id: str):
    session = db.SessionLocal()
    exp = session.query(Experiment).filter(Experiment.id == id).first()
    session.close()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp
