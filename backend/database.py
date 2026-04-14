import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

USE_AZURE = os.getenv("USE_AZURE", "false").lower() == "true"

"""
if USE_AZURE:
    DATABASE_URL = os.getenv("AZURE_SQL_URL")
    engine = create_engine(DATABASE_URL)
else:
    DATABASE_URL = os.getenv("SQLITE_URL", "sqlite:///./real_estate.db")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
"""

if USE_AZURE:
    DATABASE_URL = os.getenv("AZURE_SQL_URL")
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "timeout": 30,
        },
        pool_pre_ping=True,  # reconnects dropped connections automatically
        pool_recycle=1800,  # recycle connections every 30 min
    )
else:
    DATABASE_URL = os.getenv("SQLITE_URL", "sqlite:///./real_estate.db")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
