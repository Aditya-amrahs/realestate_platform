from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_user  # user only

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/{property_id}", response_model=schemas.FavoriteOut)
def add_favorite(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_user),  # user only
):
    existing = (
        db.query(models.Favorite)
        .filter_by(user_id=current_user.id, property_id=property_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")
    fav = models.Favorite(user_id=current_user.id, property_id=property_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


@router.delete("/{property_id}")
def remove_favorite(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_user),  # user only
):
    fav = (
        db.query(models.Favorite)
        .filter_by(user_id=current_user.id, property_id=property_id)
        .first()
    )
    if not fav:
        raise HTTPException(status_code=404, detail="Not in favorites")
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favorites"}


@router.get("/", response_model=list[schemas.FavoriteOut])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_user),  # user only
):
    return db.query(models.Favorite).filter_by(user_id=current_user.id).all()
