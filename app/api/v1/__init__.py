from fastapi import APIRouter
from app.api.v1.pets import router as pets_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(pets_router)
