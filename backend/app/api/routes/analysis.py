"""Core analysis endpoint — the main upload + analyze flow."""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.farm_scan import FarmScan
from app.utils.file_storage import save_upload, get_image_url
from app.services.image_analysis_service import image_analysis_service
from app.services.weather_service import weather_service
from app.services.soil_context_service import soil_context_service
from app.services.soil_health_service import soil_health_service
from app.services.crop_recommendation_service import crop_recommendation_service
from app.services.explanation_service import explanation_service
from app.services.vitality_service import fertilizer_service
from app.services.farm_history_service import farm_history_service

router = APIRouter()


@router.post("/analyze")
async def analyze_soil(
    image: UploadFile = File(...),
    farm_name: str = Form(default="My Farm"),
    field_name: Optional[str] = Form(default=None),
    crop_type: Optional[str] = Form(default=None),
    latitude: Optional[float] = Form(default=None),
    longitude: Optional[float] = Form(default=None),
    location_name: Optional[str] = Form(default=None),
    language: str = Form(default="en"),
    db: Session = Depends(get_db),
):
    """Upload image and run full multimodal soil analysis."""
    # 1. Save uploaded image
    try:
        file_info = await save_upload(image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Analyze image features
    image_features = image_analysis_service.analyze(file_info["path"])

    # 3. Fetch weather data
    weather_data = {}
    if latitude is not None and longitude is not None:
        weather_data = await weather_service.get_weather(latitude, longitude)
    else:
        weather_data = {
            "temperature": 28, "humidity": 55, "precipitation": 1.5,
            "wind_speed": 8, "weather_code": 1, "cloud_cover": 40,
            "uv_index": 6, "description": "Default (no location)", "is_mock": True,
        }

    # 4. Fetch soil context
    soil_ctx = {}
    if latitude is not None and longitude is not None:
        soil_ctx = await soil_context_service.get_soil_context(latitude, longitude)
    else:
        soil_ctx = {"available": False, "source": "none"}

    # 5. Compute soil health scores
    health_scores = soil_health_service.compute_health(image_features, weather_data, soil_ctx)

    # 6. Get crop recommendations
    crop_recs = crop_recommendation_service.recommend(
        moisture_level=health_scores["moisture_level"],
        fertility_level=health_scores["fertility_level"],
        temperature=weather_data.get("temperature", 25),
        nutrient_stress=health_scores["nutrient_stress"],
    )

    # 7. Get fertilizer suggestions
    fert_suggestions = fertilizer_service.suggest(
        fertility_level=health_scores["fertility_level"],
        nutrient_stress=health_scores["nutrient_stress"],
        moisture_level=health_scores["moisture_level"],
        soil_context=soil_ctx,
    )

    # 8. Generate explanation
    explanation_data = explanation_service.generate_explanation(
        image_features, weather_data, soil_ctx, health_scores, language
    )

    # 9. Save to database
    scan = FarmScan(
        farm_name=farm_name,
        field_name=field_name,
        crop_type=crop_type,
        latitude=latitude,
        longitude=longitude,
        location_name=location_name,
        image_path=file_info["path"],
        image_filename=file_info["filename"],
        vitality_score=health_scores["vitality_score"],
        moisture_level=health_scores["moisture_level"],
        fertility_level=health_scores["fertility_level"],
        nutrient_stress=health_scores["nutrient_stress"],
        irrigation_urgency=health_scores["irrigation_urgency"],
        confidence_score=health_scores["confidence_score"],
        analysis_details=health_scores,
        weather_data=weather_data,
        soil_context=soil_ctx,
        crop_recommendations=crop_recs,
        fertilizer_suggestions=fert_suggestions,
        explanation=explanation_data["explanation"],
        action_checklist=explanation_data["action_checklist"],
        image_features=image_features,
        language=language,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # 10. Return full result
    result = scan.to_dict()
    result["image_url"] = get_image_url(file_info["filename"])
    result["visual_signals"] = explanation_data["visual_signals"]
    result["weather_factors"] = explanation_data["weather_factors"]
    result["soil_priors"] = explanation_data["soil_priors"]
    return result


@router.get("/analysis/{scan_id}")
async def get_analysis(scan_id: int, db: Session = Depends(get_db)):
    """Get a specific analysis result."""
    scan = farm_history_service.get_scan_by_id(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan["image_url"] = get_image_url(scan["image_filename"])
    return scan


@router.get("/history")
async def get_history(
    farm_name: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Get scan history, optionally filtered by farm."""
    if farm_name:
        scans = farm_history_service.get_farm_scans(db, farm_name, limit)
    else:
        scans = farm_history_service.get_all_scans(db, limit)
    
    for s in scans:
        s["image_url"] = get_image_url(s["image_filename"])
    
    return {"scans": scans, "total": len(scans)}
