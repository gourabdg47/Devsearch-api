from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from api.models.custom_vertical import CustomVerticalDB, CustomVerticalCreate, CustomVerticalUpdate
from api.db.database import get_db
from typing import List, Optional
from sqlalchemy.orm import selectinload
from api.models.user import User
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class CustomVerticalService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_vertical(self, vertical: CustomVerticalCreate, user_id: int) -> CustomVerticalDB:
        try:
            db_vertical = CustomVerticalDB(**vertical.dict(), user_id=user_id)
            self.db.add(db_vertical)
            await self.db.commit()
            await self.db.refresh(db_vertical)
            return db_vertical
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating custom vertical: {str(e)}")
            raise HTTPException(status_code=500, detail="Error creating custom vertical")

    async def list_verticals(self, user_id: int) -> List[CustomVerticalDB]:
        try:
            result = await self.db.execute(select(CustomVerticalDB).where(CustomVerticalDB.user_id == user_id))
            return result.scalars().all()
        except SQLAlchemyError:
            return []

    async def get_vertical(self, vertical_id: int, user_id: int) -> Optional[CustomVerticalDB]:
        result = await self.db.execute(
            select(CustomVerticalDB).options(selectinload(CustomVerticalDB.user)).where(
                CustomVerticalDB.id == vertical_id,
                CustomVerticalDB.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def update_vertical(self, vertical_id: int, user_id: int, updated_data: CustomVerticalUpdate) -> Optional[CustomVerticalDB]:
        try:
            vertical = await self.get_vertical(vertical_id, user_id)
            if vertical:
                for key, value in updated_data.dict(exclude_unset=True).items():
                    setattr(vertical, key, value)
                await self.db.commit()
                await self.db.refresh(vertical)
            return vertical
        except SQLAlchemyError:
            await self.db.rollback()
            return None

    async def delete_vertical(self, vertical_id: int, user_id: int) -> bool:
        try:
            vertical = await self.get_vertical(vertical_id, user_id)
            if vertical:
                await self.db.delete(vertical)
                await self.db.commit()
                return True
            return False
        except SQLAlchemyError:
            await self.db.rollback()
            return False