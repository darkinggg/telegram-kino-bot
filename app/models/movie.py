from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
import random

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    file_id = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Movie(code={self.code}, id={self.id})>"