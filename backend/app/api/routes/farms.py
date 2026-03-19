"""Farm-related routes — dashboard, history, trends."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.farm_history_service import farm_history_service

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get overall dashboard summary."""
    return farm_history_service.get_dashboard_summary(db)


@router.get("/farms")
async def get_farms(db: Session = Depends(get_db)):
    """Get list of all farm names."""
    return {"farms": farm_history_service.get_farm_names(db)}


@router.get("/farms/{farm_name}/history")
async def get_farm_history(farm_name: str, db: Session = Depends(get_db)):
    """Get full history and trend data for a specific farm."""
    scans = farm_history_service.get_farm_scans(db, farm_name)
    if not scans:
        raise HTTPException(status_code=404, detail=f"No scans found for farm: {farm_name}")
    
    from app.utils.file_storage import get_image_url
    for s in scans:
        s["image_url"] = get_image_url(s["image_filename"])
    
    trend_data = farm_history_service.get_trend_data(scans)
    overall_trend = farm_history_service.compute_trend(scans)
    
    return {
        "farm_name": farm_name,
        "scans": scans,
        "trend_data": trend_data,
        "overall_trend": overall_trend,
    }
