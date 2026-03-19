"""Pydantic schemas for weather data."""
from pydantic import BaseModel
from typing import Optional


class WeatherData(BaseModel):
    temperature: float = 0.0
    humidity: float = 0.0
    precipitation: float = 0.0
    wind_speed: float = 0.0
    soil_temperature: Optional[float] = None
    soil_moisture: Optional[float] = None
    uv_index: Optional[float] = None
    cloud_cover: Optional[float] = None
    weather_code: Optional[int] = None
    description: str = "Unknown"
    is_mock: bool = False


class WeatherRequest(BaseModel):
    latitude: float
    longitude: float


class GeocodingResult(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str
    admin1: Optional[str] = None
