"""Soil health scoring service — the core prediction engine.
Combines image features, weather data, and soil context into actionable scores.
Deterministic and explainable for demo reliability."""

from app.utils.scoring import (
    clamp, level_from_score, fertility_from_score,
    urgency_from_score, compute_vitality_index,
    compute_confidence, weather_impact_score,
)


class SoilHealthService:
    """Core scoring engine combining multimodal signals."""

    def compute_health(
        self,
        image_features: dict,
        weather_data: dict,
        soil_context: dict,
    ) -> dict:
        """Compute all soil health scores from multimodal inputs."""
        
        # ── Image-derived scores ──
        moisture_score = self._compute_moisture_score(image_features, weather_data)
        fertility_score = self._compute_fertility_score(image_features, soil_context)
        vegetation_score = self._compute_vegetation_score(image_features)
        nutrient_score = self._compute_nutrient_stress_score(image_features, soil_context)
        irrigation_score = self._compute_irrigation_score(image_features, weather_data)
        
        # ── Weather score ──
        w_score = weather_impact_score(
            weather_data.get("temperature", 25),
            weather_data.get("humidity", 50),
            weather_data.get("precipitation", 0),
            weather_data.get("wind_speed", 5),
        )
        
        # ── Soil context score ──
        from app.services.soil_context_service import soil_context_service
        s_score = soil_context_service.soil_context_score(soil_context)
        
        # ── Vitality index ──
        vitality = compute_vitality_index(
            moisture_score, fertility_score, vegetation_score, w_score, s_score
        )
        
        # ── Confidence ──
        confidence = compute_confidence(
            has_weather=not weather_data.get("is_mock", True),
            has_soil_context=soil_context.get("available", False),
            image_quality=image_features.get("image_quality", 0.5),
        )
        
        return {
            "vitality_score": vitality,
            "moisture_level": level_from_score(moisture_score),
            "moisture_score": round(moisture_score, 1),
            "fertility_level": fertility_from_score(fertility_score),
            "fertility_score": round(fertility_score, 1),
            "nutrient_stress": urgency_from_score(100 - nutrient_score),  # Inverse: low score = high stress
            "nutrient_stress_score": round(100 - nutrient_score, 1),
            "irrigation_urgency": urgency_from_score(irrigation_score),
            "irrigation_score": round(irrigation_score, 1),
            "vegetation_score": round(vegetation_score, 1),
            "weather_score": round(w_score, 1),
            "soil_context_score": round(s_score, 1),
            "confidence_score": confidence,
        }

    def _compute_moisture_score(self, features: dict, weather: dict) -> float:
        """Estimate moisture 0-100 (higher = more moist)."""
        # Image signals
        dryness = features.get("dryness_cue", 0.3)
        brown = features.get("brown_ratio", 0.3)
        brightness = features.get("brightness", 0.5)
        
        img_moisture = (1.0 - dryness) * 40 + (1.0 - brown) * 30 + (1.0 - brightness) * 15
        
        # Weather contribution
        humidity = weather.get("humidity", 50)
        precip = weather.get("precipitation", 0)
        weather_moisture = humidity * 0.3 + min(precip * 5, 25)
        
        return clamp(img_moisture * 0.65 + weather_moisture * 0.35)

    def _compute_fertility_score(self, features: dict, soil_ctx: dict) -> float:
        """Estimate fertility 0-100."""
        green = features.get("green_ratio", 0.3)
        veg = features.get("vegetation_index", 0.4)
        texture = features.get("texture_score", 0.4)
        
        img_fertility = green * 120 + veg * 100 + texture * 30
        img_fertility = clamp(img_fertility / 2.5)
        
        # Soil context bonus
        ctx_bonus = 0
        if soil_ctx.get("available"):
            soc = soil_ctx.get("soc", 0)
            nitrogen = soil_ctx.get("nitrogen", 0)
            ctx_bonus = min(20, (soc / 100 + nitrogen / 500) * 10)
        
        return clamp(img_fertility + ctx_bonus)

    def _compute_vegetation_score(self, features: dict) -> float:
        """Vegetation health score 0-100."""
        green = features.get("green_ratio", 0.3)
        veg_idx = features.get("vegetation_index", 0.4)
        uniformity = features.get("color_uniformity", 0.5)
        
        score = green * 150 + veg_idx * 120 + uniformity * 30
        return clamp(score / 3.0)

    def _compute_nutrient_stress_score(self, features: dict, soil_ctx: dict) -> float:
        """Nutrient adequacy 0-100 (higher = less stress)."""
        green = features.get("green_ratio", 0.3)
        patchiness = features.get("patchiness", 0.3)
        contrast = features.get("contrast", 0.5)
        
        score = green * 120 + (1.0 - patchiness) * 80 + contrast * 30
        score = clamp(score / 2.3)
        
        if soil_ctx.get("available"):
            nitrogen = soil_ctx.get("nitrogen", 0)
            if nitrogen > 300:
                score += 10
            elif nitrogen < 100:
                score -= 10
        
        return clamp(score)

    def _compute_irrigation_score(self, features: dict, weather: dict) -> float:
        """Irrigation urgency 0-100 (higher = more urgent)."""
        dryness = features.get("dryness_cue", 0.3)
        brown = features.get("brown_ratio", 0.3)
        
        img_urgency = dryness * 100 + brown * 60
        
        # Weather: high temp + low humidity + low precip = more urgent
        temp = weather.get("temperature", 25)
        humidity = weather.get("humidity", 50)
        precip = weather.get("precipitation", 0)
        
        weather_urgency = max(0, (temp - 20) * 2) + max(0, (60 - humidity) * 0.5) + max(0, (3 - precip) * 8)
        
        return clamp((img_urgency * 0.6 + weather_urgency * 0.4) / 1.6)


soil_health_service = SoilHealthService()
