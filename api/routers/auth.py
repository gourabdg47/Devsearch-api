from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.dependencies import get_db, get_auth_service
from api.services.auth_service import AuthService, UserAlreadyExistsError
from api.config import settings
from api.models.user import UserCreate, UserInDB
from api.logger import get_logger

from api.services.auth_service import AuthService
from api.exceptions import UserAlreadyExistsError

router = APIRouter()
logger = get_logger(__name__)

@router.post("/register", response_model=UserInDB)
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        new_user = await auth_service.create_user(user)
        return new_user
    except UserAlreadyExistsError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        logger.error(f"Invalid input during registration: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input data")
    except Exception as e:
        logger.exception("Unexpected error during registration")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}