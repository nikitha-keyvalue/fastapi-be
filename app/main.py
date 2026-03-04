from fastapi import FastAPI

from app.core.config import settings
from app.routes.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(health_router, prefix="/api", tags=["health"])


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {"message": f"{settings.APP_NAME} is running"}
