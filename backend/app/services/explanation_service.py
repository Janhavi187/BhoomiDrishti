"""Explanation service — generates human-readable, explainable analysis summaries."""
from app.utils.translations import t


class ExplanationService:
    """Generate explainable AI summaries."""

    def generate_explanation(
        self,
        image_features: dict,
        weather_data: dict,
        soil_context: dict,
        health_scores: dict,
        lang: str = "en",
    ) -> dict:
        """Generate full explanation with visual signals, weather factors, reasoning, and actions."""
        
        visual_signals = self._describe_visual_signals(image_features, lang)
        weather_factors = self._describe_weather_factors(weather_data, lang)
        soil_priors = self._describe_soil_priors(soil_context, lang)
        reasoning = self._generate_reasoning(health_scores, image_features, weather_data, lang)
        actions = self._generate_action_checklist(health_scores, lang)
        
        explanation_text = self._combine_explanation(
            visual_signals, weather_factors, soil_priors, reasoning, lang
        )
        
        return {
            "explanation": explanation_text,
            "visual_signals": visual_signals,
            "weather_factors": weather_factors,
            "soil_priors": soil_priors,
            "action_checklist": actions,
        }

    def _describe_visual_signals(self, features: dict, lang: str) -> list:
        signals = []
        green = features.get("green_ratio", 0.3)
        brown = features.get("brown_ratio", 0.3)
        dryness = features.get("dryness_cue", 0.3)
        patchiness = features.get("patchiness", 0.3)
        veg = features.get("vegetation_index", 0.4)
        texture = features.get("texture_score", 0.4)

        if green > 0.4:
            signals.append("Strong green vegetation detected — healthy plant cover.")
        elif green > 0.25:
            signals.append("Moderate green coverage — some vegetation present.")
        else:
            signals.append("Low green coverage — possible bare soil or stressed vegetation.")

        if brown > 0.4:
            signals.append("Significant brown/earth tones — soil may be exposed or dry.")
        
        if dryness > 0.4:
            signals.append("Dryness indicators detected — surface appears arid or parched.")
        elif dryness < 0.15:
            signals.append("Soil appears moist — good moisture retention visible.")
        
        if patchiness > 0.3:
            signals.append("Uneven coverage — patchy growth or soil heterogeneity.")
        
        if veg > 0.55:
            signals.append("High vegetation index — strong photosynthetic activity inferred.")
        
        if texture > 0.5:
            signals.append("Rich texture detected — healthy soil structure or crop canopy.")

        return signals

    def _describe_weather_factors(self, weather: dict, lang: str) -> list:
        factors = []
        temp = weather.get("temperature", 25)
        humidity = weather.get("humidity", 50)
        precip = weather.get("precipitation", 0)
        wind = weather.get("wind_speed", 5)
        desc = weather.get("description", "Unknown")

        factors.append(f"Current weather: {desc}")
        factors.append(f"Temperature: {temp}°C — {'favorable' if 18 <= temp <= 32 else 'may affect crop growth'}")
        factors.append(f"Humidity: {humidity}% — {'adequate' if humidity > 40 else 'low, increase irrigation'}")
        
        if precip > 5:
            factors.append(f"Recent rainfall: {precip}mm — sufficient natural irrigation")
        elif precip > 0:
            factors.append(f"Light rainfall: {precip}mm — supplement with irrigation")
        else:
            factors.append("No recent rainfall — irrigation may be needed")
        
        if wind > 15:
            factors.append(f"High wind speed: {wind} km/h — risk of soil erosion")
        
        if weather.get("is_mock"):
            factors.append("Note: Using estimated weather data (API unavailable)")

        return factors

    def _describe_soil_priors(self, soil_ctx: dict, lang: str) -> list:
        if not soil_ctx.get("available"):
            return ["Soil lab data not available for this location — analysis based on visual and weather cues."]
        
        priors = [f"Soil data source: {soil_ctx.get('source', 'SoilGrids')}"]
        
        if "soil_type_estimate" in soil_ctx:
            priors.append(f"Estimated soil type: {soil_ctx['soil_type_estimate']}")
        if "phh2o" in soil_ctx:
            ph = soil_ctx["phh2o"] / 10.0
            priors.append(f"Soil pH: {ph:.1f} — {'optimal range' if 5.5 <= ph <= 7.5 else 'may need correction'}")
        if "soc" in soil_ctx:
            priors.append(f"Soil organic carbon: {soil_ctx['soc']} g/kg")
        if "nitrogen" in soil_ctx:
            priors.append(f"Nitrogen content: {soil_ctx['nitrogen']} mg/kg")

        return priors

    def _generate_reasoning(self, scores: dict, features: dict, weather: dict, lang: str) -> str:
        vitality = scores.get("vitality_score", 50)
        moisture = scores.get("moisture_level", "medium")
        fertility = scores.get("fertility_level", "moderate")
        
        if vitality >= 70:
            base = "Your farmland shows strong overall health. "
        elif vitality >= 45:
            base = "Your farmland shows moderate health with room for improvement. "
        else:
            base = "Your farmland shows signs of stress that need attention. "
        
        base += f"Moisture is {moisture}, fertility is {fertility}. "
        
        if scores.get("irrigation_urgency") == "high":
            base += "Irrigation is urgently recommended. "
        
        if scores.get("nutrient_stress") == "high":
            base += "Nutrient supplementation should be prioritized. "
        
        return base

    def _generate_action_checklist(self, scores: dict, lang: str) -> list:
        actions = []
        
        if scores.get("irrigation_urgency") in ("medium", "high"):
            actions.append("💧 Schedule irrigation within the next 24-48 hours")
        
        if scores.get("moisture_level") == "low":
            actions.append("🌊 Apply mulching to improve moisture retention")
        
        if scores.get("fertility_level") == "poor":
            actions.append("🌱 Apply organic compost or farmyard manure")
            actions.append("🧪 Consider soil testing at nearest Krishi Vigyan Kendra")
        
        if scores.get("nutrient_stress") in ("medium", "high"):
            actions.append("🧬 Apply balanced NPK fertilizer based on crop needs")
        
        if scores.get("vitality_score", 50) < 40:
            actions.append("🔬 Urgent: Get professional soil testing done")
            actions.append("📞 Contact local agriculture extension officer")
        
        actions.append("📸 Schedule next scan in 7-14 days to track progress")
        actions.append("📝 Record any treatments applied for comparison")
        
        return actions

    def _combine_explanation(self, visual, weather, soil, reasoning, lang):
        parts = [reasoning, ""]
        parts.append("🔍 Visual Analysis:")
        parts.extend([f"  • {s}" for s in visual])
        parts.append("")
        parts.append("🌤️ Weather Context:")
        parts.extend([f"  • {f}" for f in weather])
        parts.append("")
        parts.append("🧪 Soil Context:")
        parts.extend([f"  • {s}" for s in soil])
        return "\n".join(parts)


explanation_service = ExplanationService()
