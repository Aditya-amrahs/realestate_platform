from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from auth import require_agent  # dashboard = agent only

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
def agent_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_agent),  # agent only
):
    agent = db.query(models.Agent).filter_by(user_id=current_user.id).first()
    props = db.query(models.Property).filter_by(agent_id=agent.id).all()
    prop_ids = [p.id for p in props]
    total_bookings = (
        db.query(models.Booking)
        .filter(models.Booking.property_id.in_(prop_ids))
        .count()
    )
    total_views = (
        db.query(models.PropertyView)
        .filter(models.PropertyView.property_id.in_(prop_ids))
        .count()
    )
    return {
        "properties_listed": len(props),
        "total_bookings": total_bookings,
        "total_views": total_views,
    }


@router.get("/trending-locations")  # public
def trending_locations(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Property.city, func.count(models.PropertyView.id).label("views")
        )
        .join(
            models.PropertyView, models.Property.id == models.PropertyView.property_id
        )
        .group_by(models.Property.city)
        .order_by(func.count(models.PropertyView.id).desc())
        .limit(10)
        .all()
    )
    return [{"city": r.city, "views": r.views} for r in results]
