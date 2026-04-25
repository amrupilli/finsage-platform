from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api import warnings
from app.api.auth import router as auth_router
from app.api.onboarding import router as onboarding_router
from app.core.config import get_settings
from app.db.database import get_db

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Finsage educational digital investing platform.",
    version=settings.app_version,
)

# ✅ ADD THIS (CORS MIDDLEWARE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing routers (UNCHANGED)
app.include_router(auth_router)
app.include_router(onboarding_router)
app.include_router(warnings.router)

# Health endpoints (UNCHANGED)
@app.get("/health")
def health_check() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "debug": settings.debug,
    }


@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"database_status": "ok"}