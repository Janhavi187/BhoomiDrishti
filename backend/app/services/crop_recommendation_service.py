"""Crop recommendation service — suggests best crops based on soil/weather analysis."""


CROP_DATABASE = [
    {
        "crop": "Rice (Paddy)",
        "min_moisture": "medium", "ideal_moisture": "high",
        "min_fertility": "moderate", "ideal_temp": (22, 32),
        "season": "Kharif (Jun-Nov)",
        "sustainability": "High water requirement — consider SRI method for water savings.",
    },
    {
        "crop": "Wheat",
        "min_moisture": "medium", "ideal_moisture": "medium",
        "min_fertility": "moderate", "ideal_temp": (12, 25),
        "season": "Rabi (Nov-Apr)",
        "sustainability": "Relatively lower water need. Good for crop rotation with legumes.",
    },
    {
        "crop": "Maize (Corn)",
        "min_moisture": "medium", "ideal_moisture": "medium",
        "min_fertility": "moderate", "ideal_temp": (18, 30),
        "season": "Kharif / Rabi",
        "sustainability": "Versatile crop. Stalks can be used for composting.",
    },
    {
        "crop": "Millets (Bajra/Jowar)",
        "min_moisture": "low", "ideal_moisture": "low",
        "min_fertility": "poor", "ideal_temp": (25, 40),
        "season": "Kharif (Jun-Sep)",
        "sustainability": "Highly drought-resistant. Excellent for dry regions. Nutritious superfood.",
    },
    {
        "crop": "Groundnut (Peanut)",
        "min_moisture": "low", "ideal_moisture": "medium",
        "min_fertility": "poor", "ideal_temp": (20, 30),
        "season": "Kharif (Jun-Oct)",
        "sustainability": "Nitrogen-fixing legume. Improves soil health naturally.",
    },
    {
        "crop": "Soybean",
        "min_moisture": "medium", "ideal_moisture": "medium",
        "min_fertility": "moderate", "ideal_temp": (20, 30),
        "season": "Kharif (Jun-Oct)",
        "sustainability": "Excellent nitrogen fixer. Good rotation crop.",
    },
    {
        "crop": "Cotton",
        "min_moisture": "low", "ideal_moisture": "medium",
        "min_fertility": "moderate", "ideal_temp": (22, 35),
        "season": "Kharif (Apr-Oct)",
        "sustainability": "Consider organic cotton practices. High water need in conventional farming.",
    },
    {
        "crop": "Sugarcane",
        "min_moisture": "high", "ideal_moisture": "high",
        "min_fertility": "good", "ideal_temp": (20, 35),
        "season": "Perennial (12-18 months)",
        "sustainability": "Very high water requirement. Drip irrigation recommended.",
    },
    {
        "crop": "Pulses (Moong/Urad)",
        "min_moisture": "low", "ideal_moisture": "medium",
        "min_fertility": "poor", "ideal_temp": (25, 35),
        "season": "Kharif / Rabi / Zaid",
        "sustainability": "Nitrogen fixation enriches soil. Short duration crop.",
    },
    {
        "crop": "Vegetables (Leafy Greens)",
        "min_moisture": "medium", "ideal_moisture": "high",
        "min_fertility": "good", "ideal_temp": (15, 30),
        "season": "Year-round",
        "sustainability": "Intercropping potential. Quick harvest cycle.",
    },
    {
        "crop": "Tomato",
        "min_moisture": "medium", "ideal_moisture": "medium",
        "min_fertility": "good", "ideal_temp": (18, 30),
        "season": "Rabi / Summer",
        "sustainability": "Mulching reduces water need. Stake for better yield.",
    },
    {
        "crop": "Mustard",
        "min_moisture": "low", "ideal_moisture": "low",
        "min_fertility": "moderate", "ideal_temp": (10, 25),
        "season": "Rabi (Oct-Mar)",
        "sustainability": "Low water need. Good bee-pollinator crop.",
    },
]

MOISTURE_ORDER = {"low": 0, "medium": 1, "high": 2}
FERTILITY_ORDER = {"poor": 0, "moderate": 1, "good": 2}


class CropRecommendationService:
    def recommend(
        self,
        moisture_level: str,
        fertility_level: str,
        temperature: float,
        nutrient_stress: str,
    ) -> list:
        """Return ranked list of crop recommendations."""
        recommendations = []
        
        for crop in CROP_DATABASE:
            score, reasons = self._score_crop(
                crop, moisture_level, fertility_level, temperature, nutrient_stress
            )
            suitability = self._suitability_label(score)
            
            recommendations.append({
                "crop": crop["crop"],
                "suitability": suitability,
                "score": score,
                "reason": "; ".join(reasons),
                "season": crop["season"],
                "sustainability_note": crop["sustainability"],
            })
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top 6
        return recommendations[:6]

    def _score_crop(self, crop: dict, moisture: str, fertility: str, temp: float, nutrient_stress: str) -> tuple:
        score = 50.0
        reasons = []
        
        # Moisture match
        m_current = MOISTURE_ORDER.get(moisture, 1)
        m_min = MOISTURE_ORDER.get(crop["min_moisture"], 1)
        m_ideal = MOISTURE_ORDER.get(crop["ideal_moisture"], 1)
        
        if m_current >= m_min:
            score += 15
            if m_current == m_ideal:
                score += 10
                reasons.append(f"Ideal moisture match ({moisture})")
            else:
                reasons.append(f"Adequate moisture ({moisture})")
        else:
            score -= 15
            reasons.append(f"Moisture too low for optimal {crop['crop']} growth")
        
        # Fertility match
        f_current = FERTILITY_ORDER.get(fertility, 1)
        f_min = FERTILITY_ORDER.get(crop["min_fertility"], 1)
        
        if f_current >= f_min:
            score += 15
            reasons.append(f"Soil fertility sufficient ({fertility})")
        else:
            score -= 10
            reasons.append(f"Fertility may be insufficient — consider enrichment")
        
        # Temperature match
        ideal_low, ideal_high = crop["ideal_temp"]
        if ideal_low <= temp <= ideal_high:
            score += 15
            reasons.append(f"Temperature {temp}°C within ideal range")
        elif ideal_low - 5 <= temp <= ideal_high + 5:
            score += 5
            reasons.append(f"Temperature {temp}°C near acceptable range")
        else:
            score -= 10
            reasons.append(f"Temperature {temp}°C outside ideal range ({ideal_low}-{ideal_high}°C)")
        
        # Nutrient stress
        if nutrient_stress == "high" and FERTILITY_ORDER.get(crop["min_fertility"], 1) >= 2:
            score -= 10
            reasons.append("High nutrient stress may limit yield")
        elif nutrient_stress == "low":
            score += 5
        
        return max(0, min(100, score)), reasons

    def _suitability_label(self, score: float) -> str:
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "moderate"
        return "poor"


crop_recommendation_service = CropRecommendationService()
