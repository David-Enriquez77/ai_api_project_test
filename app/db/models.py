from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
#User and Prediction models for the database
# These models define the structure of the database tables for users and their predictions.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    predictions = relationship("Prediction", back_populates="user")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    sepal_length = Column(Float)
    sepal_width = Column(Float)
    petal_length = Column(Float)
    petal_width = Column(Float)
    predicted_class = Column(Integer)
    predicted_label = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="predictions")
    user_id = Column(Integer, ForeignKey("users.id"))