"""Application configuration with environment variable support."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)

class Settings:
    APP_NAME: str = "BhoomiDrishti AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_DIR}/bhoomi_drishti.db")
    
    # File storage
    UPLOAD_DIR: Path = UPLOAD_DIR
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "webp", "bmp"}
    
    # External APIs
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    OPEN_METEO_GEOCODING_URL: str = "https://geocoding-api.open-meteo.com/v1"
    SOILGRIDS_BASE_URL: str = "https://rest.isric.org/soilgrids/v2.0"
    
    # Timeouts
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "10"))
    
    # Static files
    STATIC_URL: str = "/static"
    REPORTS_DIR: Path = BASE_DIR / "reports"

    def __init__(self):
        self.REPORTS_DIR.mkdir(exist_ok=True)

settings = Settings()
