"""Report generation routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.farm_history_service import farm_history_service
from app.services.report_service import report_service

router = APIRouter()


@router.get("/report/{scan_id}")
async def generate_report(
    scan_id: int,
    language: str = Query(default="en"),
    db: Session = Depends(get_db),
):
    """Generate and return an HTML report for a scan."""
    scan = farm_history_service.get_scan_by_id(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    html = report_service.generate_html_report(scan, language)
    url = report_service.save_report(scan_id, html)
    
    from datetime import datetime
    return {
        "scan_id": scan_id,
        "report_url": url,
        "format": "html",
        "generated_at": datetime.now().isoformat(),
    }


@router.get("/report/{scan_id}/html")
async def get_report_html(
    scan_id: int,
    language: str = Query(default="en"),
    db: Session = Depends(get_db),
):
    """Return raw HTML report content."""
    scan = farm_history_service.get_scan_by_id(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    html = report_service.generate_html_report(scan, language)
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html)
