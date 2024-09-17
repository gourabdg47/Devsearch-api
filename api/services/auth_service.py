from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from api.config import settings
from api.models.user import User, UserCreate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from argon2 import PasswordHasher
import logging
import traceback

from api.exceptions import UserAlreadyExistsError

ph = PasswordHasher()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user or not self.verify_password(password, user.password):
            return False
        return user

    async def get_user(self, username: str):
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    def verify_password(self, plain_password, password):
        try:
            return ph.verify(password, plain_password)
        except:
            return False

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def create_user(self, user: UserCreate) -> UserInDB:
        logger.info(f"Creating user: {user.dict()}")
        existing_user = await self.get_user(user.username)
        if existing_user:
            raise UserAlreadyExistsError("Username already registered")
        
        hashed_password = self.get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, password=hashed_password)
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        
        return UserInDB.from_orm(new_user)

    def get_password_hash(self, password: str) -> str:
        return ph.hash(password)