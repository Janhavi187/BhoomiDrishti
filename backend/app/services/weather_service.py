"""Weather service — fetches real-time weather from Open-Meteo with fallback."""
import httpx
import json
from pathlib import Path
from app.core.config import settings

MOCK_WEATHER_PATH = Path(__file__).parent.parent / "demo" / "mock_weather.json"


class WeatherService:
    """Fetch weather data from Open-Meteo API with mock fallback."""

    async def get_weather(self, lat: float, lon: float) -> dict:
        """Get current weather for coordinates."""
        try:
            async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code,cloud_cover",
                    "daily": "uv_index_max",
                    "timezone": "auto",
                    "forecast_days": 1,
                }
                resp = await client.get(f"{settings.OPEN_METEO_BASE_URL}/forecast", params=params)
                resp.raise_for_status()
                data = resp.json()

                current = data.get("current", {})
                daily = data.get("daily", {})

                return {
                    "temperature": current.get("temperature_2m", 25),
                    "humidity": current.get("relative_humidity_2m", 50),
                    "precipitation": current.get("precipitation", 0),
                    "wind_speed": current.get("wind_speed_10m", 5),
                    "weather_code": current.get("weather_code", 0),
                    "cloud_cover": current.get("cloud_cover", 50),
                    "uv_index": daily.get("uv_index_max", [5])[0] if daily.get("uv_index_max") else 5,
                    "description": self._weather_code_to_desc(current.get("weather_code", 0)),
                    "is_mock": False,
                }
        except Exception as e:
            print(f"[WeatherService] Open-Meteo API failed: {e}. Using mock data.")
            return self._get_mock_weather(lat, lon)

    async def geocode(self, query: str) -> list:
        """Geocode a location name to coordinates."""
        try:
            async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
                params = {"name": query, "count": 5, "language": "en"}
                resp = await client.get(f"{settings.OPEN_METEO_GEOCODING_URL}/search", params=params)
                resp.raise_for_status()
                data = resp.json()
                results = data.get("results", [])
                return [
                    {
                        "name": r.get("name", ""),
                        "latitude": r.get("latitude", 0),
                        "longitude": r.get("longitude", 0),
                        "country": r.get("country", ""),
                        "admin1": r.get("admin1", ""),
                    }
                    for r in results
                ]
        except Exception as e:
            print(f"[WeatherService] Geocoding failed: {e}")
            return []

    def _get_mock_weather(self, lat: float, lon: float) -> dict:
        """Load mock weather data as fallback."""
        try:
            with open(MOCK_WEATHER_PATH, "r") as f:
                mock_data = json.load(f)
            # Select region based on latitude
            if lat > 25:
                region = "north_india"
            elif lat > 15:
                region = "central_india"
            else:
                region = "south_india"
            weather = mock_data.get(region, mock_data.get("default", {}))
            weather["is_mock"] = True
            return weather
        except Exception:
            return {
                "temperature": 28,
                "humidity": 55,
                "precipitation": 1.5,
                "wind_speed": 8,
                "weather_code": 1,
                "cloud_cover": 40,
                "uv_index": 6,
                "description": "Partly cloudy (mock)",
                "is_mock": True,
            }

    def _weather_code_to_desc(self, code: int) -> str:
        """Convert WMO weather code to description."""
        codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
        }
        return codes.get(code, "Unknown")


weather_service = WeatherService()
