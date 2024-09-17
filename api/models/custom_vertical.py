from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from api.db.database import Base

class CustomVerticalCreate(BaseModel):
    name: str
    description: str
    query_fields: List[str]
    filters: Optional[dict] = None

class CustomVerticalUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    query_fields: Optional[List[str]] = None
    filters: Optional[dict] = None

class CustomVerticalResponse(CustomVerticalCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class CustomVerticalDB(Base):
    __tablename__ = "custom_verticals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    query_fields = Column(JSON)
    filters = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="custom_verticals")

    __table_args__ = (Index('idx_user_id', user_id),)