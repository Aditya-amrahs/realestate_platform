from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import models, schemas
from auth import require_agent
from vector_store import build_index


router = APIRouter(prefix="/properties", tags=["Properties"])


@router.post("/", response_model=schemas.PropertyOut)
def create_property(
    payload: schemas.PropertyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_agent),
):
    agent = db.query(models.Agent).filter_by(user_id=current_user.id).first()
    prop = models.Property(**payload.dict(), agent_id=agent.id)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    all_props = db.query(models.Property).all()  #
    build_index(all_props)  # rebuild FAISS index with new property
    return prop


@router.get("/", response_model=list[schemas.PropertyOut])  # public
def list_properties(
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    type: Optional[str] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Property)
    if city:
        q = q.filter(models.Property.city.ilike(f"%{city}%"))
    if min_price:
        q = q.filter(models.Property.price >= min_price)
    if max_price:
        q = q.filter(models.Property.price <= max_price)
    if type:
        q = q.filter(models.Property.type == type)
    if min_size:
        q = q.filter(models.Property.size >= min_size)
    if max_size:
        q = q.filter(models.Property.size <= max_size)
    return q.all()


@router.get("/{property_id}", response_model=schemas.PropertyOut)  # public
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    view = models.PropertyView(property_id=property_id)
    db.add(view)
    db.commit()
    return prop


@router.put("/{property_id}", response_model=schemas.PropertyOut)
def update_property(
    property_id: int,
    payload: schemas.PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_agent),
):
    agent = db.query(models.Agent).filter_by(user_id=current_user.id).first()
    prop = (
        db.query(models.Property).filter_by(id=property_id, agent_id=agent.id).first()
    )
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found or not yours")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(prop, field, value)
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_agent),
):
    agent = db.query(models.Agent).filter_by(user_id=current_user.id).first()
    prop = (
        db.query(models.Property).filter_by(id=property_id, agent_id=agent.id).first()
    )
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found or not yours")
    db.delete(prop)
    db.commit()
    all_props = db.query(models.Property).all()  #
    build_index(all_props)  # rebuild FAISS index after deletion
    return {"message": "Property deleted"}
