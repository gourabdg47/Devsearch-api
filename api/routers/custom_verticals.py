from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.models.custom_vertical import CustomVerticalResponse, CustomVerticalCreate
from api.services.custom_vertical_service import CustomVerticalService
from api.dependencies import get_custom_vertical_service, get_current_user
from api.models.user import User
import logging

router = APIRouter()

@router.post("/", response_model=CustomVerticalResponse)
async def create_custom_vertical(
    vertical: CustomVerticalCreate,
    service: CustomVerticalService = Depends(get_custom_vertical_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.create_vertical(vertical, current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Unexpected error creating custom vertical: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/", response_model=List[CustomVerticalResponse])
async def list_custom_verticals(
    service: CustomVerticalService = Depends(get_custom_vertical_service),
    current_user: User = Depends(get_current_user)
):
    return await service.list_verticals(current_user.id)

@router.get("/{vertical_id}", response_model=CustomVerticalResponse)
async def get_custom_vertical(
    vertical_id: int,
    service: CustomVerticalService = Depends(get_custom_vertical_service),
    current_user: User = Depends(get_current_user)
):
    vertical = await service.get_vertical(vertical_id, current_user.id)
    if not vertical:
        raise HTTPException(status_code=404, detail="Custom vertical not found")
    return vertical