from fastapi import FastAPI

app = FastAPI(
    title="Finsage Platform API",
    description="Backend API for the Finsage educational digital investing platform.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}