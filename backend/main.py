import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
import models
from routers import auth, properties, bookings, favorites, analytics, recommendations

# vector store
from vector_store import build_index
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", ""),  # have to set this in azure app settings
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(bookings.router)
app.include_router(favorites.router)
app.include_router(analytics.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {"message": "Real Estate API is running"}


# for FAISS index, we build it on startup and whenever a new property is added.
@app.on_event("startup")
def startup_event():
    db: Session = Session(bind=engine)
    try:
        properties = db.query(models.Property).all()
        build_index(properties)
        print(f"Built FAISS index for {len(properties)} properties")
    finally:
        db.close()
