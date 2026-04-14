from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(20), default="user")

    agent = relationship("Agent", back_populates="user", uselist=False)
    bookings = relationship("Booking", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="agent")
    properties = relationship("Property", back_populates="agent")


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    city = Column(String(100), index=True)
    price = Column(Float, index=True)
    type = Column(String(50))
    size = Column(Integer)
    image_url = Column(String(500), nullable=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))

    agent = relationship("Agent", back_populates="properties")
    bookings = relationship("Booking", back_populates="property")
    favorites = relationship("Favorite", back_populates="property")
    views = relationship("PropertyView", back_populates="property")


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))

    __table_args__ = (UniqueConstraint("user_id", "property_id"),)

    user = relationship("User", back_populates="favorites")
    property = relationship("Property", back_populates="favorites")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    visit_date = Column(Date)
    visit_time = Column(Time)

    user = relationship("User", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")


class PropertyView(Base):
    __tablename__ = "property_views"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    viewed_at = Column(DateTime, server_default=func.now())

    property = relationship("Property", back_populates="views")
