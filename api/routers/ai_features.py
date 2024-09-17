import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from api.dependencies import get_ai_service, get_current_user
from api.models.user import User
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()

class SummarizeResponse(BaseModel):
    summary: str

@router.get("/summarize", response_model=SummarizeResponse)
async def summarize_text(
    text: str = Query(..., min_length=1),
    max_length: int = Query(150, ge=30, le=500),
    ai_service = Depends(get_ai_service),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Summarizing text for user: {current_user.username}")
        summary = await ai_service.summarize(text, max_length)
        return SummarizeResponse(summary=summary)
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during summarization")