from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from .base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, full_name={self.full_name})>"