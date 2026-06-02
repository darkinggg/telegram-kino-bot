from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Enum as SQLEnum
from .base import Base
import random
import enum

class Category(str, enum.Enum):
    DRAMA = "Drama"
    COMEDY = "Komediya"
    ACTION = "Aksyon"
    THRILLER = "Thriller"
    ROMANCE = "Sevgi"
    HORROR = "Qo'rquv"
    SCI_FI = "Fantastika"
    ANIMATED = "Multfilm"

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    file_id = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    director = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)
    category = Column(SQLEnum(Category), nullable=True)
    description = Column(Text, nullable=True)
    rating = Column(Float, default=0.0, nullable=False)
    total_ratings = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Movie(code={self.code}, title={self.title})>"