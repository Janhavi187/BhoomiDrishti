"""SQLAlchemy model for farm scans — the core data entity."""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class FarmScan(Base):
    __tablename__ = "farm_scans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Farm info
    farm_name = Column(String(255), nullable=False, default="My Farm")
    field_name = Column(String(255), nullable=True)
    crop_type = Column(String(100), nullable=True)
    
    # Location
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_name = Column(String(255), nullable=True)
    
    # Image
    image_path = Column(String(500), nullable=False)
    image_filename = Column(String(255), nullable=False)
    
    # Analysis results (stored as JSON for flexibility)
    vitality_score = Column(Float, nullable=True)
    moisture_level = Column(String(50), nullable=True)
    fertility_level = Column(String(50), nullable=True)
    nutrient_stress = Column(String(50), nullable=True)
    irrigation_urgency = Column(String(50), nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Detailed results
    analysis_details = Column(JSON, nullable=True)
    weather_data = Column(JSON, nullable=True)
    soil_context = Column(JSON, nullable=True)
    crop_recommendations = Column(JSON, nullable=True)
    fertilizer_suggestions = Column(JSON, nullable=True)
    explanation = Column(Text, nullable=True)
    action_checklist = Column(JSON, nullable=True)
    
    # Image features extracted
    image_features = Column(JSON, nullable=True)
    
    # Metadata
    language = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "farm_name": self.farm_name,
            "field_name": self.field_name,
            "crop_type": self.crop_type,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_name": self.location_name,
            "image_filename": self.image_filename,
            "image_path": self.image_path,
            "vitality_score": self.vitality_score,
            "moisture_level": self.moisture_level,
            "fertility_level": self.fertility_level,
            "nutrient_stress": self.nutrient_stress,
            "irrigation_urgency": self.irrigation_urgency,
            "confidence_score": self.confidence_score,
            "analysis_details": self.analysis_details,
            "weather_data": self.weather_data,
            "soil_context": self.soil_context,
            "crop_recommendations": self.crop_recommendations,
            "fertilizer_suggestions": self.fertilizer_suggestions,
            "explanation": self.explanation,
            "action_checklist": self.action_checklist,
            "image_features": self.image_features,
            "language": self.language,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
