# 🌾 BhoomiDrishti AI

## A Multimodal Virtual Soil Lab & Digital Farmland Twin for Smallholder Farmers

> **Aligned with UN SDG 2 — Zero Hunger** | Sensorless Soil Intelligence | Explainable Agro AI

[![SDG 2](https://img.shields.io/badge/UN%20SDG-2%20Zero%20Hunger-green?style=for-the-badge)](https://sdgs.un.org/goals/goal2)
[![Python](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python-blue?style=for-the-badge)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%20%2B%20TypeScript-black?style=for-the-badge)](https://nextjs.org)

---

## 🚀 What is BhoomiDrishti AI?

BhoomiDrishti AI transforms **smartphone-captured images** into actionable agricultural intelligence — predicting soil health, crop suitability, irrigation urgency, and fertility levels **without expensive sensors or physical labs**.

### Key Capabilities
- 🔬 **Virtual Soil Lab** — Analyze soil from a photo
- 🗺️ **Digital Farmland Twin** — Track farm health over time
- 🧠 **Explainable AI** — Transparent reasoning for every recommendation
- 🌾 **Smart Crop Advisor** — Data-driven crop and fertilizer suggestions
- 🌤️ **Weather-Enriched** — Real-time weather integration
- 🌐 **Multilingual** — English, Hindi, Tamil support
- 📄 **Report Export** — Downloadable HTML reports

---

## 🎯 SDG 2 Alignment

This platform directly contributes to **Zero Hunger** by:
- Empowering **500M+ smallholder farmers** globally with accessible soil intelligence
- Eliminating the need for expensive lab testing or IoT sensors
- Providing **hyperlocal, actionable** agricultural recommendations
- Supporting **sustainable farming** through data-driven insights

---

## 🏗️ Architecture

```
bhoomi-drishti-ai/
├── backend/                     # FastAPI + Python
│   ├── app/
│   │   ├── main.py              # Application entry point
│   │   ├── core/
│   │   │   ├── config.py        # Settings + env vars
│   │   │   └── database.py      # SQLAlchemy + SQLite
│   │   ├── api/routes/
│   │   │   ├── health.py        # Health check
│   │   │   ├── analysis.py      # Upload + analyze + history
│   │   │   ├── farms.py         # Dashboard + farm management
│   │   │   ├── weather.py       # Weather proxy
│   │   │   ├── reports.py       # Report generation
│   │   │   └── insights.py      # Regional insights
│   │   ├── services/
│   │   │   ├── image_analysis_service.py   # PIL-based CV features
│   │   │   ├── weather_service.py          # Open-Meteo integration
│   │   │   ├── soil_context_service.py     # SoilGrids integration
│   │   │   ├── soil_health_service.py      # Core scoring engine
│   │   │   ├── crop_recommendation_service.py
│   │   │   ├── explanation_service.py      # Explainable AI
│   │   │   ├── vitality_service.py         # Fertilizer suggestions
│   │   │   ├── farm_history_service.py     # Trends + history
│   │   │   ├── regional_insights_service.py
│   │   │   └── report_service.py           # HTML report generation
│   │   ├── models/
│   │   │   └── farm_scan.py     # SQLAlchemy model
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── utils/
│   │   │   ├── file_storage.py  # Upload handling
│   │   │   ├── scoring.py       # Deterministic scoring
│   │   │   └── translations.py  # i18n (EN/HI/TA)
│   │   └── demo/
│   │       ├── seed_data.py     # Demo data generator
│   │       ├── mock_weather.json
│   │       └── mock_regions.json
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                    # Next.js + TypeScript + Tailwind
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # Landing page
│   │   │   ├── dashboard/       # Dashboard
│   │   │   ├── upload/          # Image upload flow
│   │   │   ├── analysis/[id]/   # Analysis results
│   │   │   ├── history/         # Scan history
│   │   │   └── insights/        # Regional insights
│   │   └── lib/
│   │       ├── api.ts           # API client + types
│   │       ├── i18n.ts          # Translations
│   │       └── utils.ts         # Color + format utilities
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

---

## ⚡ Quick Start (Local)

### Prerequisites
- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)

### 1. Backend Setup

```bash
# Terminal 1
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or (Mac/Linux)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will:
- Create SQLite database automatically
- Generate sample images
- Seed demo data (7 scans across 3 farms)
- Serve API at `http://localhost:8000`
- API docs at `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Terminal 2
cd frontend

# Install dependencies
npm install

# Copy env file
cp .env.example .env.local

# Start dev server
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## 🐳 Docker Setup

```bash
# From project root
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

---

## 🧪 Test Checklist

After starting both servers:

| # | Test | How |
|---|------|-----|
| 1 | Landing page loads | Open `http://localhost:3000` |
| 2 | Dashboard shows data | Click "Dashboard" — seed data shows |
| 3 | Upload works | Go to "New Scan" → upload any image |
| 4 | Analysis results | Automatic redirect after upload |
| 5 | Charts render | Check radar chart + bar charts on results |
| 6 | History page | Click "History" → see all scans |
| 7 | Farm filter | Filter by farm name in History |
| 8 | Regional insights | Click "Regional Insights" |
| 9 | Report download | Click "Download Report" on any result |
| 10 | Language switch | Change language to Hindi or Tamil |
| 11 | API docs | Visit `http://localhost:8000/docs` |
| 12 | Health check | GET `http://localhost:8000/api/health` |
| 13 | Mobile responsive | Resize browser to mobile width |
| 14 | Empty state | Works with no data (before seed) |

### Sample API Requests

```bash
# Health check
curl http://localhost:8000/api/health

# Dashboard
curl http://localhost:8000/api/dashboard

# Weather
curl "http://localhost:8000/api/weather?lat=28.6139&lon=77.2090"

# Geocode
curl "http://localhost:8000/api/geocode?q=Delhi"

# Regional insights
curl http://localhost:8000/api/insights/regional

# Upload + analyze
curl -X POST http://localhost:8000/api/analyze \
  -F "image=@path/to/photo.jpg" \
  -F "farm_name=Test Farm" \
  -F "latitude=28.6139" \
  -F "longitude=77.2090" \
  -F "location_name=Delhi"

# History
curl http://localhost:8000/api/history

# Report
curl http://localhost:8000/api/report/1/html
```

---

## 🧠 AI/Scoring Logic

The MVP uses a **hybrid heuristic approach** — not a trained model, but real visual analysis:

### Image Features Extracted (PIL/NumPy)
- **Brightness** — overall light level
- **Contrast** — variation in pixel values
- **Green Ratio** — vegetation detection
- **Brown Ratio** — exposed soil detection
- **Texture Score** — edge-based complexity
- **Patchiness** — spatial uniformity
- **Dryness Cue** — arid surface indicators
- **Vegetation Index** — simplified VARI proxy
- **Image Quality** — brightness/contrast adequacy

### Enrichment Sources
- **Open-Meteo** — real-time temperature, humidity, precipitation, wind
- **SoilGrids** — clay/sand/silt, pH, organic carbon, nitrogen

### Scoring Engine
- **Moisture Score** — image dryness + weather humidity + rainfall
- **Fertility Score** — vegetation + soil organic carbon + nitrogen
- **Nutrient Stress** — patchiness + green ratio + nitrogen levels
- **Irrigation Urgency** — dryness + temperature + rainfall deficit
- **Vitality Index** — weighted composite of all scores (0-100)
- **Confidence** — data completeness (weather + soil + image quality)

All scoring is **deterministic** for demo stability and fully **explainable**.

---

## 🔮 Future Scope with NVIDIA Acceleration

The architecture is designed for easy ML model integration:

1. **CNN/ViT Model** — Replace `image_analysis_service.py` with a trained PyTorch/TensorFlow model
2. **NVIDIA TensorRT** — Optimize inference for real-time analysis
3. **Satellite Imagery** — Scale from smartphone to satellite using NVIDIA DALI for data loading
4. **Edge Deployment** — Run on NVIDIA Jetson for offline field analysis
5. **Multi-spectral** — Integrate NIR/SWIR bands for advanced soil analysis

---

## 🌐 Multilingual Support

Currently supported:
- 🇬🇧 **English** (complete)
- 🇮🇳 **Hindi** (major UI labels)
- 🇮🇳 **Tamil** (major UI labels)

Adding a new language requires only adding entries to:
- `backend/app/utils/translations.py`
- `frontend/src/lib/i18n.ts`

---

## 📝 Technical Feasibility

| Aspect | Status |
|--------|--------|
| Image analysis | ✅ Real PIL-based feature extraction |
| Weather integration | ✅ Live Open-Meteo API + mock fallback |
| Soil context | ✅ SoilGrids API + graceful degradation |
| Database | ✅ SQLite with auto-migration |
| Reports | ✅ Styled HTML generation |
| Charts | ✅ Recharts (radar, bar, line, pie) |
| Multilingual | ✅ EN/HI/TA with switcher |
| Error handling | ✅ Full fallback chain |
| Responsive | ✅ Mobile-friendly with bottom nav |
| Docker | ✅ Full compose setup |

---

## 📜 License

MIT License — Built for hackathon demonstration purposes.

---

**🌾 BhoomiDrishti AI — Empowering every farmer with AI intelligence, one smartphone photo at a time.**
#   B h o o m i D r i s h t i  
 