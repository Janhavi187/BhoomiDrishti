"""Weather routes — proxy to weather service."""
from fastapi import APIRouter, Query
from app.services.weather_service import weather_service

router = APIRouter()


@router.get("/weather")
async def get_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    """Get current weather for coordinates."""
    data = await weather_service.get_weather(lat, lon)
    return data


@router.get("/geocode")
async def geocode(q: str = Query(..., min_length=2)):
    """Geocode a location name."""
    results = await weather_service.geocode(q)
    return {"results": results}
