"""Regional insights service — provides mocked regional summary data."""
import json
from pathlib import Path

MOCK_REGIONS_PATH = Path(__file__).parent.parent / "demo" / "mock_regions.json"


class RegionalInsightsService:
    """Provide regional agricultural insights (demo data)."""

    def get_regional_insights(self) -> dict:
        """Return mock regional data."""
        try:
            with open(MOCK_REGIONS_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return self._default_insights()

    def _default_insights(self) -> dict:
        return {
            "regions": [
                {
                    "name": "Punjab",
                    "state": "Punjab",
                    "avg_vitality": 72,
                    "dominant_crop": "Wheat",
                    "stress_level": "low",
                    "total_scans": 124,
                    "moisture_trend": "stable",
                    "alert": None,
                },
                {
                    "name": "Vidarbha",
                    "state": "Maharashtra",
                    "avg_vitality": 41,
                    "dominant_crop": "Cotton",
                    "stress_level": "high",
                    "total_scans": 89,
                    "moisture_trend": "degrading",
                    "alert": "Drought stress detected — irrigation advisory issued",
                },
                {
                    "name": "Thanjavur Delta",
                    "state": "Tamil Nadu",
                    "avg_vitality": 68,
                    "dominant_crop": "Rice",
                    "stress_level": "medium",
                    "total_scans": 156,
                    "moisture_trend": "improving",
                    "alert": None,
                },
                {
                    "name": "Malwa Plateau",
                    "state": "Madhya Pradesh",
                    "avg_vitality": 55,
                    "dominant_crop": "Soybean",
                    "stress_level": "medium",
                    "total_scans": 67,
                    "moisture_trend": "stable",
                    "alert": "Moderate nutrient depletion noted",
                },
                {
                    "name": "Bundelkhand",
                    "state": "Uttar Pradesh",
                    "avg_vitality": 35,
                    "dominant_crop": "Millets",
                    "stress_level": "high",
                    "total_scans": 43,
                    "moisture_trend": "degrading",
                    "alert": "Severe water stress — emergency measures recommended",
                },
                {
                    "name": "Konkan Coast",
                    "state": "Maharashtra",
                    "avg_vitality": 78,
                    "dominant_crop": "Rice",
                    "stress_level": "low",
                    "total_scans": 91,
                    "moisture_trend": "stable",
                    "alert": None,
                },
            ],
            "national_avg_vitality": 58.2,
            "total_scans_nationwide": 570,
            "hotspots": [
                {"region": "Bundelkhand", "issue": "Water Stress", "severity": "critical"},
                {"region": "Vidarbha", "issue": "Drought", "severity": "high"},
                {"region": "Malwa Plateau", "issue": "Nutrient Depletion", "severity": "moderate"},
            ],
            "last_updated": "2026-03-18T18:00:00Z",
        }


regional_insights_service = RegionalInsightsService()
