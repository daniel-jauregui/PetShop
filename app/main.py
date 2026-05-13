from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import Base, engine
import app.models  # noqa: F401 — ensure all models are registered with Base


def create_app() -> FastAPI:
    # Create all tables on startup (migrate properly with Alembic in production)
    Base.metadata.create_all(bind=engine)

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    application.include_router(api_router)
    application.mount("/static", StaticFiles(directory="static"), name="static")

    @application.get("/", tags=["Health"])
    def health():
        return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}

    return application


app = create_app()
