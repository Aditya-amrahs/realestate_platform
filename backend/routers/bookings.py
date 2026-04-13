from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import require_user  # user only

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=schemas.BookingOut)
def book_visit(
    payload: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_user),  # user only
):
    conflict = (
        db.query(models.Booking)
        .filter_by(
            property_id=payload.property_id,
            visit_date=payload.visit_date,
            visit_time=payload.visit_time,
        )
        .first()
    )
    if conflict:
        raise HTTPException(status_code=400, detail="Slot already booked")
    booking = models.Booking(
        user_id=current_user.id,
        property_id=payload.property_id,
        visit_date=payload.visit_date,
        visit_time=payload.visit_time,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/", response_model=list[schemas.BookingOut])
def my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_user),  # user only
):
    return db.query(models.Booking).filter_by(user_id=current_user.id).all()
