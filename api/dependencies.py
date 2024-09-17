from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

import sys
import os

from jose import jwt, JWTError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Import your models here
from api.models.custom_vertical import CustomVerticalDB
from api.models.user import User
from api.config import settings

from api.db.database import get_db
from api.services.search_engine import SearchEngine
from api.services.custom_vertical_service import CustomVerticalService
from api.services.ai_service import AIService
from api.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

search_engine = SearchEngine()
ai_service = None #AIService()

async def get_search_engine():
    try:
        yield search_engine
    finally:
        await search_engine.close()

def get_custom_vertical_service(db: AsyncSession = Depends(get_db)):
    return CustomVerticalService(db)

async def get_ai_service():
    global ai_service
    if ai_service is None:
        ai_service = AIService()
    return ai_service

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    auth_service = AuthService(db)
    user = await auth_service.get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def authenticate_user(token: str, db: AsyncSession):
    # Implement your user authentication logic here
    # This is a placeholder implementation
    return User(id=1, username="testuser", email="test@example.com")

def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)