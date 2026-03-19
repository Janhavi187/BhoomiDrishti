"""Scoring utilities for deterministic soil health scoring."""
import math


def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(max_val, value))


def level_from_score(score: float, thresholds: tuple = (35, 65)) -> str:
    """Convert 0-100 score to low/medium/high."""
    if score < thresholds[0]:
        return "low"
    elif score < thresholds[1]:
        return "medium"
    return "high"


def fertility_from_score(score: float) -> str:
    if score < 35:
        return "poor"
    elif score < 65:
        return "moderate"
    return "good"


def urgency_from_score(score: float) -> str:
    """Higher score = more urgent."""
    if score < 30:
        return "low"
    elif score < 60:
        return "medium"
    return "high"


def compute_vitality_index(
    moisture_score: float,
    fertility_score: float,
    vegetation_score: float,
    weather_score: float,
    soil_context_score: float = 50.0,
) -> float:
    """
    Weighted composite score 0-100.
    Weights tuned for demo stability.
    """
    weights = {
        "moisture": 0.20,
        "fertility": 0.25,
        "vegetation": 0.25,
        "weather": 0.15,
        "soil_context": 0.15,
    }
    raw = (
        moisture_score * weights["moisture"]
        + fertility_score * weights["fertility"]
        + vegetation_score * weights["vegetation"]
        + weather_score * weights["weather"]
        + soil_context_score * weights["soil_context"]
    )
    return round(clamp(raw), 1)


def compute_confidence(
    has_weather: bool,
    has_soil_context: bool,
    image_quality: float,
) -> float:
    """Compute confidence score 0-1."""
    base = 0.55
    if has_weather:
        base += 0.15
    if has_soil_context:
        base += 0.10
    base += image_quality * 0.20
    return round(clamp(base, 0.0, 1.0), 2)


def weather_impact_score(temp: float, humidity: float, precip: float, wind: float) -> float:
    """Score weather favorability for agriculture 0-100."""
    temp_score = 100 - abs(temp - 25) * 3  # Ideal ~25°C
    humidity_score = 100 - abs(humidity - 60) * 1.5  # Ideal ~60%
    precip_score = 100 - abs(precip - 3) * 10  # Ideal ~3mm
    wind_score = max(0, 100 - wind * 5)  # Lower wind better
    
    score = (temp_score * 0.3 + humidity_score * 0.3 + precip_score * 0.2 + wind_score * 0.2)
    return round(clamp(score), 1)
