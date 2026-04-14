from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from vector_store import get_similar, build_index

router = APIRouter(prefix="/properties", tags=["Recommendations"])


@router.get("/{property_id}/similar", response_model=list[schemas.PropertyOut])
def similar_properties(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    similar_ids = get_similar(property_id, top_k=5)
    if not similar_ids:
        return []

    return db.query(models.Property).filter(models.Property.id.in_(similar_ids)).all()


@router.post("/rebuild-index")
def rebuild_index(db: Session = Depends(get_db)):
    """Call this after adding new properties to refresh the FAISS index."""
    properties = db.query(models.Property).all()
    build_index(properties)
    return {"message": f"Index rebuilt with {len(properties)} properties."}
