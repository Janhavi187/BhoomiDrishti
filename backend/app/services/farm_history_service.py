"""Farm history service — tracks scans over time and computes trends."""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.farm_scan import FarmScan


class FarmHistoryService:
    """Manage farm scan history and compute trends."""

    def get_farm_scans(self, db: Session, farm_name: str, limit: int = 50) -> list:
        """Get all scans for a farm, ordered by date."""
        scans = (
            db.query(FarmScan)
            .filter(FarmScan.farm_name == farm_name)
            .order_by(desc(FarmScan.created_at))
            .limit(limit)
            .all()
        )
        return [s.to_dict() for s in scans]

    def get_all_scans(self, db: Session, limit: int = 50) -> list:
        scans = (
            db.query(FarmScan)
            .order_by(desc(FarmScan.created_at))
            .limit(limit)
            .all()
        )
        return [s.to_dict() for s in scans]

    def get_scan_by_id(self, db: Session, scan_id: int) -> dict | None:
        scan = db.query(FarmScan).filter(FarmScan.id == scan_id).first()
        return scan.to_dict() if scan else None

    def get_farm_names(self, db: Session) -> list:
        results = db.query(FarmScan.farm_name).distinct().all()
        return [r[0] for r in results]

    def compute_trend(self, scans: list) -> str:
        """Determine if farm health is improving, stable, or degrading."""
        if len(scans) < 2:
            return "stable"
        
        scores = [s.get("vitality_score", 50) for s in scans if s.get("vitality_score")]
        if len(scores) < 2:
            return "stable"
        
        # Compare recent vs older (scans are newest-first)
        recent = sum(scores[:len(scores)//2]) / max(1, len(scores)//2)
        older = sum(scores[len(scores)//2:]) / max(1, len(scores) - len(scores)//2)
        
        diff = recent - older
        if diff > 5:
            return "improving"
        elif diff < -5:
            return "degrading"
        return "stable"

    def get_trend_data(self, scans: list) -> list:
        """Extract trend data points for charting."""
        points = []
        for scan in reversed(scans):  # Chronological order
            points.append({
                "scan_id": scan.get("id"),
                "date": scan.get("created_at", ""),
                "vitality_score": scan.get("vitality_score", 0),
                "moisture_level": scan.get("moisture_level", "medium"),
                "fertility_level": scan.get("fertility_level", "moderate"),
            })
        return points

    def get_dashboard_summary(self, db: Session) -> dict:
        """Get overall dashboard summary."""
        all_scans = self.get_all_scans(db, limit=100)
        farms = self.get_farm_names(db)
        
        if not all_scans:
            return {
                "total_scans": 0,
                "total_farms": 0,
                "avg_vitality": 0,
                "latest_scan": None,
                "trend": "stable",
                "farms": [],
            }
        
        scores = [s.get("vitality_score", 0) for s in all_scans if s.get("vitality_score")]
        avg_vitality = sum(scores) / len(scores) if scores else 0
        
        farm_summaries = []
        for farm in farms:
            farm_scans = [s for s in all_scans if s.get("farm_name") == farm]
            if farm_scans:
                farm_scores = [s.get("vitality_score", 0) for s in farm_scans if s.get("vitality_score")]
                farm_summaries.append({
                    "farm_name": farm,
                    "total_scans": len(farm_scans),
                    "latest_vitality": farm_scans[0].get("vitality_score"),
                    "avg_vitality": round(sum(farm_scores) / len(farm_scores), 1) if farm_scores else 0,
                    "latest_moisture": farm_scans[0].get("moisture_level"),
                    "latest_fertility": farm_scans[0].get("fertility_level"),
                    "trend": self.compute_trend(farm_scans),
                })
        
        return {
            "total_scans": len(all_scans),
            "total_farms": len(farms),
            "avg_vitality": round(avg_vitality, 1),
            "latest_scan": all_scans[0] if all_scans else None,
            "trend": self.compute_trend(all_scans),
            "farms": farm_summaries,
        }


farm_history_service = FarmHistoryService()
