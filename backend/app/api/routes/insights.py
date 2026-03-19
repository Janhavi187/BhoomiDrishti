"""Regional insights routes."""
from fastapi import APIRouter
from app.services.regional_insights_service import regional_insights_service

router = APIRouter()


@router.get("/insights/regional")
async def get_regional_insights():
    """Get regional agricultural insights (demo data)."""
    return regional_insights_service.get_regional_insights()
