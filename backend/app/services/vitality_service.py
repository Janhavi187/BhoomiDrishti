"""Fertilizer suggestion service."""


FERTILIZER_DATABASE = {
    "nitrogen_low": {
        "fertilizer": "Urea (46-0-0) or DAP",
        "dosage": "50-60 kg/acre",
        "timing": "Apply in 2-3 split doses during growth stages",
        "reason": "Low nitrogen detected — essential for leaf growth and chlorophyll production.",
    },
    "nitrogen_medium": {
        "fertilizer": "NPK 20-20-20 balanced",
        "dosage": "30-40 kg/acre",
        "timing": "Apply during vegetative growth phase",
        "reason": "Moderate nitrogen — maintain with balanced application.",
    },
    "phosphorus_low": {
        "fertilizer": "Single Super Phosphate (SSP)",
        "dosage": "40-50 kg/acre",
        "timing": "Apply at sowing/planting time as basal dose",
        "reason": "Phosphorus supports root development and flowering.",
    },
    "potassium_low": {
        "fertilizer": "Muriate of Potash (MOP)",
        "dosage": "25-35 kg/acre",
        "timing": "Apply 50% basal + 50% at flowering",
        "reason": "Potassium improves disease resistance and crop quality.",
    },
    "organic": {
        "fertilizer": "Farmyard Manure (FYM) or Vermicompost",
        "dosage": "2-3 tonnes/acre",
        "timing": "Apply 2-3 weeks before sowing",
        "reason": "Organic matter improves soil structure, water retention, and microbial activity.",
    },
    "micronutrient": {
        "fertilizer": "Micronutrient mixture (Zn, Fe, Mn, B)",
        "dosage": "5-10 kg/acre or foliar spray",
        "timing": "Foliar application during growth phase",
        "reason": "Micronutrients prevent deficiency symptoms and boost yield.",
    },
}


class FertilizerService:
    def suggest(
        self,
        fertility_level: str,
        nutrient_stress: str,
        moisture_level: str,
        soil_context: dict,
    ) -> list:
        suggestions = []
        
        # Always recommend organic
        suggestions.append(FERTILIZER_DATABASE["organic"])
        
        if fertility_level == "poor":
            suggestions.append(FERTILIZER_DATABASE["nitrogen_low"])
            suggestions.append(FERTILIZER_DATABASE["phosphorus_low"])
            suggestions.append(FERTILIZER_DATABASE["potassium_low"])
        elif fertility_level == "moderate":
            suggestions.append(FERTILIZER_DATABASE["nitrogen_medium"])
            if nutrient_stress in ("medium", "high"):
                suggestions.append(FERTILIZER_DATABASE["phosphorus_low"])
        
        if nutrient_stress == "high":
            suggestions.append(FERTILIZER_DATABASE["micronutrient"])
        
        # Soil context adjustments
        if soil_context.get("available"):
            ph = soil_context.get("phh2o", 0)
            if ph:
                ph_val = ph / 10.0
                if ph_val < 5.5:
                    suggestions.append({
                        "fertilizer": "Agricultural Lime",
                        "dosage": "100-200 kg/acre",
                        "timing": "Apply 2-4 weeks before sowing",
                        "reason": f"Soil pH is {ph_val:.1f} (acidic) — lime raises pH for better nutrient availability.",
                    })
                elif ph_val > 8.0:
                    suggestions.append({
                        "fertilizer": "Gypsum (Calcium Sulphate)",
                        "dosage": "100-150 kg/acre",
                        "timing": "Apply before sowing with irrigation",
                        "reason": f"Soil pH is {ph_val:.1f} (alkaline) — gypsum helps reduce alkalinity.",
                    })
        
        return suggestions


fertilizer_service = FertilizerService()
