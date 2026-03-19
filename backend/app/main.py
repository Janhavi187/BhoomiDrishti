"""BhoomiDrishti AI — FastAPI Application Entry Point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path

from app.core.config import settings
from app.core.database import init_db, SessionLocal
from app.api.routes import health, analysis, farms, weather, reports, insights


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print(f"🌾 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    init_db()
    
    # Seed demo data
    db = SessionLocal()
    try:
        from app.demo.seed_data import seed_database
        seed_database(db, settings.UPLOAD_DIR)
    except Exception as e:
        print(f"[Seed] Warning: Could not seed data: {e}")
    finally:
        db.close()
    
    print(f"✅ Server ready at http://{settings.HOST}:{settings.PORT}")
    print(f"📖 API docs at http://{settings.HOST}:{settings.PORT}/docs")
    yield
    # Shutdown
    print("👋 Shutting down BhoomiDrishti AI")


app = FastAPI(
    title=settings.APP_NAME,
    description="🌾 Virtual Soil Lab & Digital Farmland Twin — AI for Zero Hunger (SDG 2)",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
uploads_dir = settings.UPLOAD_DIR
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

reports_dir = settings.REPORTS_DIR
reports_dir.mkdir(exist_ok=True)
app.mount("/reports", StaticFiles(directory=str(reports_dir)), name="reports")

# Routes
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(farms.router, prefix="/api", tags=["Farms"])
app.include_router(weather.router, prefix="/api", tags=["Weather"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])
app.include_router(insights.router, prefix="/api", tags=["Insights"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Virtual Soil Lab & Digital Farmland Twin",
        "docs": "/docs",
        "health": "/api/health",
    }
