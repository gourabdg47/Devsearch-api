from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from api.routers import search, custom_verticals, ai_features, auth, documentation, root, analytics
from api.config import settings
from api.logger import setup_logging, get_logger
from api.metrics import MetricsMiddleware, metrics_endpoint

app = FastAPI(title="DevSearch API", version="1.0.0")

setup_logging()
logger = get_logger(__name__)

# Mount static files
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.dirname(current_dir)
static_dir = os.path.join(project_root, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics middleware
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(custom_verticals.router, prefix="/api/v1/custom", tags=["custom"])
app.include_router(ai_features.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(documentation.router, prefix="/api/v1", tags=["documentation"])
app.include_router(root.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])

# Metrics endpoint
app.add_api_route("/metrics", metrics_endpoint, include_in_schema=False)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DevSearch API")
    uvicorn.run(app, host="0.0.0.0", port=8000)