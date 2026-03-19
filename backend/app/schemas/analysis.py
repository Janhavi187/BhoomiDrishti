"""Pydantic schemas for analysis request/response."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AnalysisRequest(BaseModel):
    farm_name: str = Field(default="My Farm", max_length=255)
    field_name: Optional[str] = Field(default=None, max_length=255)
    crop_type: Optional[str] = Field(default=None, max_length=100)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    location_name: Optional[str] = Field(default=None, max_length=255)
    language: str = Field(default="en", max_length=10)


class ImageFeatures(BaseModel):
    brightness: float = 0.0
    contrast: float = 0.0
    green_ratio: float = 0.0
    brown_ratio: float = 0.0
    texture_score: float = 0.0
    patchiness: float = 0.0
    dryness_cue: float = 0.0
    color_uniformity: float = 0.0
    vegetation_index: float = 0.0


class CropRecommendation(BaseModel):
    crop: str
    suitability: str  # "excellent", "good", "moderate", "poor"
    reason: str
    season: Optional[str] = None
    sustainability_note: Optional[str] = None


class FertilizerSuggestion(BaseModel):
    fertilizer: str
    dosage: str
    timing: str
    reason: str


class AnalysisResult(BaseModel):
    id: int
    farm_name: str
    field_name: Optional[str]
    crop_type: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    location_name: Optional[str]
    image_filename: str
    image_url: str

    # Scores
    vitality_score: float
    moisture_level: str
    fertility_level: str
    nutrient_stress: str
    irrigation_urgency: str
    confidence_score: float

    # Detailed
    weather_data: Optional[Dict[str, Any]] = None
    soil_context: Optional[Dict[str, Any]] = None
    crop_recommendations: Optional[List[Dict[str, Any]]] = None
    fertilizer_suggestions: Optional[List[Dict[str, Any]]] = None
    explanation: Optional[str] = None
    action_checklist: Optional[List[str]] = None
    image_features: Optional[Dict[str, Any]] = None
    analysis_details: Optional[Dict[str, Any]] = None

    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class AnalysisListItem(BaseModel):
    id: int
    farm_name: str
    field_name: Optional[str]
    crop_type: Optional[str]
    location_name: Optional[str]
    vitality_score: Optional[float]
    moisture_level: Optional[str]
    fertility_level: Optional[str]
    image_filename: str
    created_at: Optional[str]

    class Config:
        from_attributes = True


class TrendDataPoint(BaseModel):
    scan_id: int
    date: str
    vitality_score: float
    moisture_level: str
    fertility_level: str
