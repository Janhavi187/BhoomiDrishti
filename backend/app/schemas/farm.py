"""Pydantic schemas for farm-related data."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class FarmSummary(BaseModel):
    farm_name: str
    total_scans: int
    latest_vitality: Optional[float]
    avg_vitality: Optional[float]
    latest_moisture: Optional[str]
    latest_fertility: Optional[str]
    trend: str  # "improving", "stable", "degrading"
    scans: List[Dict[str, Any]]


class FarmHistoryResponse(BaseModel):
    farm_name: str
    scans: List[Dict[str, Any]]
    trend_data: List[Dict[str, Any]]
    overall_trend: str
