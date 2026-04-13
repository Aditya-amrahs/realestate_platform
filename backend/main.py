from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, properties, bookings, favorites, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(bookings.router)
app.include_router(favorites.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Real Estate API is running"}
