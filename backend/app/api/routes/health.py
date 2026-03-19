"""Health check endpoint."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "BhoomiDrishti AI",
        "version": "1.0.0",
    }


@router.get("/languages")
async def get_languages():
    from app.utils.translations import get_supported_languages
    return {"languages": get_supported_languages()}
