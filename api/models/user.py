from sqlalchemy import Column, Integer, String
from api.db.database import Base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    custom_verticals = relationship("CustomVerticalDB", back_populates="user")
    search_logs = relationship("SearchLog", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

# Pydantic models for user operations
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True