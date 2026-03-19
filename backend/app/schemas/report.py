"""Pydantic schemas for report generation."""
from pydantic import BaseModel
from typing import Optional


class ReportRequest(BaseModel):
    scan_id: int
    language: str = "en"
    format: str = "html"  # "html" or "pdf"


class ReportResponse(BaseModel):
    scan_id: int
    report_url: str
    format: str
    generated_at: str
