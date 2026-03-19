"""Soil context service — fetches soil property priors from SoilGrids API."""
import httpx
from app.core.config import settings


class SoilContextService:
    """Fetch background soil property data from ISRIC SoilGrids REST API."""

    async def get_soil_context(self, lat: float, lon: float) -> dict:
        """Get soil properties for given coordinates. Returns empty on failure."""
        try:
            async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
                params = {
                    "lat": lat,
                    "lon": lon,
                    "property": "clay,sand,silt,soc,phh2o,nitrogen,cec",
                    "depth": "0-5cm",
                    "value": "mean",
                }
                resp = await client.get(
                    f"{settings.SOILGRIDS_BASE_URL}/properties/query",
                    params=params,
                )
                resp.raise_for_status()
                data = resp.json()
                return self._parse_soilgrids(data)
        except Exception as e:
            print(f"[SoilContextService] SoilGrids API failed: {e}. Continuing without soil context.")
            return self._empty_context()

    def _parse_soilgrids(self, data: dict) -> dict:
        """Parse SoilGrids response into simplified dict."""
        try:
            properties = data.get("properties", {}).get("layers", [])
            result = {"available": True, "source": "SoilGrids"}
            for layer in properties:
                name = layer.get("name", "")
                depths = layer.get("depths", [])
                if depths:
                    value = depths[0].get("values", {}).get("mean")
                    if value is not None:
                        result[name] = value
            
            # Derive soil type estimate
            clay = result.get("clay", 0)
            sand = result.get("sand", 0)
            silt = result.get("silt", 0)
            if clay and sand and silt:
                total = clay + sand + silt
                if total > 0:
                    if sand / total > 0.6:
                        result["soil_type_estimate"] = "Sandy"
                    elif clay / total > 0.4:
                        result["soil_type_estimate"] = "Clay"
                    elif silt / total > 0.5:
                        result["soil_type_estimate"] = "Silty"
                    else:
                        result["soil_type_estimate"] = "Loamy"
            
            return result
        except Exception:
            return self._empty_context()

    def _empty_context(self) -> dict:
        return {"available": False, "source": "none"}

    def soil_context_score(self, context: dict) -> float:
        """Convert soil context to a 0-100 favorability score."""
        if not context.get("available"):
            return 50.0  # Neutral when unavailable
        
        score = 50.0
        # pH near 6.5 is ideal
        ph = context.get("phh2o", 0)
        if ph:
            ph_val = ph / 10.0  # SoilGrids pH in pH*10
            score += max(-20, min(20, 20 - abs(ph_val - 6.5) * 8))
        
        # Higher SOC is better
        soc = context.get("soc", 0)
        if soc:
            score += min(15, soc / 50.0 * 15)
        
        # Higher nitrogen is better
        nitrogen = context.get("nitrogen", 0)
        if nitrogen:
            score += min(15, nitrogen / 500.0 * 15)
        
        return max(0, min(100, score))


soil_context_service = SoilContextService()
