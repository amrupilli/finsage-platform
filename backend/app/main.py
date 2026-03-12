from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Finsage educational digital investing platform.",
    version=settings.app_version,
)


@app.get("/health")
def health_check() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "debug": settings.debug,
    }