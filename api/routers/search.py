from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from api.models.search_result import SearchResult
from api.services.search_engine import SearchEngine
from api.dependencies import get_search_engine, get_current_user
from api.models.user import User

router = APIRouter()

@router.get("/", response_model=List[SearchResult])
async def search(
    q: str = Query(..., min_length=1, max_length=100),
    vertical: str = Query("web", description="Search vertical"),
    limit: int = Query(10, ge=1, le=100),
    search_engine: SearchEngine = Depends(get_search_engine),
    current_user: User = Depends(get_current_user)
):
    try:
        results = await search_engine.search(q, vertical, limit)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))