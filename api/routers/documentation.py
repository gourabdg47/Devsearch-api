from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from api.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Get the directory of the current file
current_dir = os.path.dirname(os.path.realpath(__file__))
# Go up two levels to the project root
project_root = os.path.dirname(os.path.dirname(current_dir))

@router.get("/documentation", include_in_schema=True)
async def serve_documentation():
    file_path = os.path.join(project_root, "static", "documentation.html")
    logger.info(f"Attempting to serve documentation from: {file_path}")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        logger.error(f"Documentation file not found at {file_path}")
        raise HTTPException(status_code=404, detail="Documentation not found")