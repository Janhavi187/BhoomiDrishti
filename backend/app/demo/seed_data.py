"""Seed data generator — creates demo scans for immediate dashboard content."""
import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from pathlib import Path


def create_sample_images(upload_dir: Path) -> list:
    """Generate sample soil/field images for demo purposes."""
    samples = []
    configs = [
        {"name": "healthy_field", "colors": [(34, 139, 34), (50, 160, 50), (60, 180, 60)], "label": "Healthy Green Field"},
        {"name": "dry_soil", "colors": [(139, 90, 43), (160, 110, 60), (180, 130, 70)], "label": "Dry Brown Soil"},
        {"name": "mixed_field", "colors": [(100, 140, 50), (130, 110, 60), (80, 150, 55)], "label": "Mixed Vegetation"},
        {"name": "wet_soil", "colors": [(60, 50, 40), (70, 60, 50), (50, 45, 35)], "label": "Moist Dark Soil"},
        {"name": "stressed_crop", "colors": [(160, 150, 50), (140, 130, 60), (170, 140, 45)], "label": "Stressed Yellow Crop"},
    ]

    for cfg in configs:
        filename = f"sample_{cfg['name']}.png"
        filepath = upload_dir / filename
        if not filepath.exists():
            img = Image.new("RGB", (400, 400))
            draw = ImageDraw.Draw(img)
            # Create patches of color
            for y in range(0, 400, 20):
                for x in range(0, 400, 20):
                    color = random.choice(cfg["colors"])
                    # Add natural variation
                    c = tuple(max(0, min(255, c + random.randint(-20, 20))) for c in color)
                    draw.rectangle([x, y, x+20, y+20], fill=c)
            img.save(filepath)
        samples.append({"filename": filename, "path": str(filepath), "label": cfg["label"]})

    return samples


def seed_database(db_session, upload_dir: Path):
    """Seed database with demo scan data."""
    from app.models.farm_scan import FarmScan
    from app.services.image_analysis_service import image_analysis_service
    from app.services.soil_health_service import soil_health_service

    # Check if already seeded
    existing = db_session.query(FarmScan).count()
    if existing > 0:
        print(f"[Seed] Database already has {existing} scans. Skipping seed.")
        return

    print("[Seed] Creating sample images and seeding database...")
    samples = create_sample_images(upload_dir)

    demo_entries = [
        {
            "farm_name": "Green Valley Farm",
            "field_name": "North Plot",
            "crop_type": "Wheat",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "location_name": "Delhi, India",
            "sample_idx": 0,
            "days_ago": 21,
        },
        {
            "farm_name": "Green Valley Farm",
            "field_name": "South Plot",
            "crop_type": "Rice",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "location_name": "Delhi, India",
            "sample_idx": 2,
            "days_ago": 14,
        },
        {
            "farm_name": "Green Valley Farm",
            "field_name": "North Plot",
            "crop_type": "Wheat",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "location_name": "Delhi, India",
            "sample_idx": 0,
            "days_ago": 7,
        },
        {
            "farm_name": "Sunrise Organic Farm",
            "field_name": "Main Field",
            "crop_type": "Millets",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "location_name": "Bangalore, India",
            "sample_idx": 1,
            "days_ago": 18,
        },
        {
            "farm_name": "Sunrise Organic Farm",
            "field_name": "Riverside",
            "crop_type": "Vegetables",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "location_name": "Bangalore, India",
            "sample_idx": 3,
            "days_ago": 10,
        },
        {
            "farm_name": "Kisan Field",
            "field_name": "Plot A",
            "crop_type": "Cotton",
            "latitude": 20.5937,
            "longitude": 78.9629,
            "location_name": "Nagpur, India",
            "sample_idx": 4,
            "days_ago": 5,
        },
        {
            "farm_name": "Kisan Field",
            "field_name": "Plot B",
            "crop_type": "Soybean",
            "latitude": 20.5937,
            "longitude": 78.9629,
            "location_name": "Nagpur, India",
            "sample_idx": 2,
            "days_ago": 2,
        },
    ]

    mock_weathers = [
        {"temperature": 24, "humidity": 50, "precipitation": 1, "wind_speed": 10, "description": "Partly cloudy", "is_mock": True},
        {"temperature": 30, "humidity": 65, "precipitation": 3, "wind_speed": 6, "description": "Light rain", "is_mock": True},
        {"temperature": 22, "humidity": 45, "precipitation": 0, "wind_speed": 12, "description": "Clear sky", "is_mock": True},
        {"temperature": 28, "humidity": 72, "precipitation": 5, "wind_speed": 5, "description": "Rain showers", "is_mock": True},
        {"temperature": 35, "humidity": 30, "precipitation": 0, "wind_speed": 15, "description": "Hot and dry", "is_mock": True},
        {"temperature": 32, "humidity": 40, "precipitation": 0, "wind_speed": 8, "description": "Mainly clear", "is_mock": True},
        {"temperature": 26, "humidity": 58, "precipitation": 2, "wind_speed": 7, "description": "Partly cloudy", "is_mock": True},
    ]

    for i, entry in enumerate(demo_entries):
        sample = samples[entry["sample_idx"]]
        weather = mock_weathers[i]
        soil_ctx = {"available": False, "source": "none"}

        # Analyze the sample image
        features = image_analysis_service.analyze(sample["path"])
        health = soil_health_service.compute_health(features, weather, soil_ctx)

        from app.services.crop_recommendation_service import crop_recommendation_service
        from app.services.vitality_service import fertilizer_service
        from app.services.explanation_service import explanation_service

        crop_recs = crop_recommendation_service.recommend(
            health["moisture_level"], health["fertility_level"],
            weather["temperature"], health["nutrient_stress"],
        )
        fert_sug = fertilizer_service.suggest(
            health["fertility_level"], health["nutrient_stress"],
            health["moisture_level"], soil_ctx,
        )
        expl = explanation_service.generate_explanation(features, weather, soil_ctx, health)

        created_at = datetime.utcnow() - timedelta(days=entry["days_ago"])

        scan = FarmScan(
            farm_name=entry["farm_name"],
            field_name=entry["field_name"],
            crop_type=entry["crop_type"],
            latitude=entry["latitude"],
            longitude=entry["longitude"],
            location_name=entry["location_name"],
            image_path=sample["path"],
            image_filename=sample["filename"],
            vitality_score=health["vitality_score"],
            moisture_level=health["moisture_level"],
            fertility_level=health["fertility_level"],
            nutrient_stress=health["nutrient_stress"],
            irrigation_urgency=health["irrigation_urgency"],
            confidence_score=health["confidence_score"],
            analysis_details=health,
            weather_data=weather,
            soil_context=soil_ctx,
            crop_recommendations=crop_recs,
            fertilizer_suggestions=fert_sug,
            explanation=expl["explanation"],
            action_checklist=expl["action_checklist"],
            image_features=features,
            language="en",
        )
        scan.created_at = created_at
        db_session.add(scan)

    db_session.commit()
    print(f"[Seed] Successfully seeded {len(demo_entries)} demo scans.")
