from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to DevSearch API"}

@router.get("/test")
async def test_route():
    logger.info("Test route accessed")
    return {"message": "Test route is working"}