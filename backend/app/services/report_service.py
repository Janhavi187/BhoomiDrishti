"""Report generation service — creates downloadable HTML reports."""
from datetime import datetime
from pathlib import Path
from app.core.config import settings
from app.utils.translations import t


class ReportService:
    """Generate printable/downloadable HTML reports for scan results."""

    def generate_html_report(self, scan_data: dict, lang: str = "en") -> str:
        """Generate a full HTML report for a scan."""
        vitality = scan_data.get("vitality_score", 0)
        vitality_color = "#22c55e" if vitality >= 65 else "#eab308" if vitality >= 40 else "#ef4444"
        
        recommendations_html = ""
        crops = scan_data.get("crop_recommendations", []) or []
        for crop in crops[:5]:
            suit_color = {"excellent": "#22c55e", "good": "#84cc16", "moderate": "#eab308", "poor": "#ef4444"}.get(crop.get("suitability", "moderate"), "#888")
            recommendations_html += f"""
            <div style="border:1px solid #e5e7eb;border-radius:8px;padding:12px;margin:8px 0;">
                <strong>{crop.get('crop', '')}</strong>
                <span style="background:{suit_color};color:white;padding:2px 8px;border-radius:12px;font-size:12px;margin-left:8px;">{crop.get('suitability', '').upper()}</span>
                <p style="margin:4px 0;font-size:13px;color:#666;">{crop.get('reason', '')}</p>
                <p style="margin:2px 0;font-size:12px;color:#888;">Season: {crop.get('season', 'N/A')}</p>
            </div>"""

        actions_html = ""
        actions = scan_data.get("action_checklist", []) or []
        for action in actions:
            actions_html += f'<li style="margin:6px 0;">{action}</li>'

        fertilizer_html = ""
        fertilizers = scan_data.get("fertilizer_suggestions", []) or []
        for fert in fertilizers:
            fertilizer_html += f"""
            <div style="border-left:3px solid #22c55e;padding:8px 12px;margin:8px 0;background:#f0fdf4;">
                <strong>{fert.get('fertilizer', '')}</strong><br>
                <span style="font-size:13px;">Dosage: {fert.get('dosage', '')} | Timing: {fert.get('timing', '')}</span><br>
                <span style="font-size:12px;color:#666;">{fert.get('reason', '')}</span>
            </div>"""

        weather = scan_data.get("weather_data", {}) or {}
        weather_html = f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div>🌡️ Temperature: {weather.get('temperature', 'N/A')}°C</div>
            <div>💧 Humidity: {weather.get('humidity', 'N/A')}%</div>
            <div>🌧️ Precipitation: {weather.get('precipitation', 'N/A')}mm</div>
            <div>💨 Wind: {weather.get('wind_speed', 'N/A')} km/h</div>
        </div>
        """

        html = f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BhoomiDrishti AI — Soil Analysis Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; color: #1a1a1a; padding: 40px; max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #22c55e; padding-bottom: 20px; }}
        .header h1 {{ color: #166534; font-size: 28px; }}
        .header p {{ color: #666; margin-top: 5px; }}
        .section {{ margin: 24px 0; }}
        .section h2 {{ color: #166534; font-size: 18px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; margin-bottom: 12px; }}
        .vitality-circle {{ width: 120px; height: 120px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 36px; font-weight: bold; color: white; }}
        .metrics {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin: 16px 0; }}
        .metric {{ text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px; }}
        .metric .label {{ font-size: 12px; color: #888; text-transform: uppercase; }}
        .metric .value {{ font-size: 20px; font-weight: 600; margin-top: 4px; }}
        .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #888; font-size: 12px; }}
        @media print {{ body {{ padding: 20px; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌾 {t('app_name', lang)} — Soil Analysis Report</h1>
        <p>{t('tagline', lang)}</p>
        <p style="margin-top:8px;font-size:14px;">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>

    <div class="section">
        <h2>📋 Scan Information</h2>
        <p><strong>Farm:</strong> {scan_data.get('farm_name', 'N/A')}</p>
        <p><strong>Field:</strong> {scan_data.get('field_name', 'N/A')}</p>
        <p><strong>Crop:</strong> {scan_data.get('crop_type', 'N/A')}</p>
        <p><strong>Location:</strong> {scan_data.get('location_name', 'N/A')} ({scan_data.get('latitude', 'N/A')}, {scan_data.get('longitude', 'N/A')})</p>
    </div>

    <div class="section" style="text-align:center;">
        <h2>🏆 {t('vitality_score', lang)}</h2>
        <div class="vitality-circle" style="background:{vitality_color};">
            {vitality:.0f}
        </div>
        <p style="margin-top:8px;color:#666;">out of 100</p>
    </div>

    <div class="section">
        <h2>📊 Key Metrics</h2>
        <div class="metrics">
            <div class="metric">
                <div class="label">{t('moisture_level', lang)}</div>
                <div class="value">{scan_data.get('moisture_level', 'N/A').upper()}</div>
            </div>
            <div class="metric">
                <div class="label">{t('fertility_level', lang)}</div>
                <div class="value">{scan_data.get('fertility_level', 'N/A').upper()}</div>
            </div>
            <div class="metric">
                <div class="label">{t('nutrient_stress', lang)}</div>
                <div class="value">{scan_data.get('nutrient_stress', 'N/A').upper()}</div>
            </div>
            <div class="metric">
                <div class="label">{t('irrigation_urgency', lang)}</div>
                <div class="value">{scan_data.get('irrigation_urgency', 'N/A').upper()}</div>
            </div>
            <div class="metric">
                <div class="label">{t('confidence', lang)}</div>
                <div class="value">{(scan_data.get('confidence_score', 0) * 100):.0f}%</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🌤️ {t('weather_context', lang)}</h2>
        {weather_html}
    </div>

    <div class="section">
        <h2>🌾 {t('crop_recommendations', lang)}</h2>
        {recommendations_html if recommendations_html else '<p>No crop recommendations available.</p>'}
    </div>

    <div class="section">
        <h2>🧪 {t('fertilizer_suggestions', lang)}</h2>
        {fertilizer_html if fertilizer_html else '<p>No fertilizer suggestions available.</p>'}
    </div>

    <div class="section">
        <h2>✅ {t('action_checklist', lang)}</h2>
        <ul style="list-style:none;padding:0;">
            {actions_html if actions_html else '<li>No actions required at this time.</li>'}
        </ul>
    </div>

    <div class="section">
        <h2>💡 {t('explanation', lang)}</h2>
        <div style="white-space:pre-wrap;font-size:14px;line-height:1.6;background:#f8fafc;padding:16px;border-radius:8px;">
{scan_data.get('explanation', 'No detailed explanation available.')}
        </div>
    </div>

    <div class="footer">
        <p>🌾 BhoomiDrishti AI — Virtual Soil Lab & Digital Farmland Twin</p>
        <p>Aligned with UN SDG 2: Zero Hunger</p>
        <p>This report is generated by AI analysis and should be used alongside professional agricultural advice.</p>
    </div>
</body>
</html>"""
        return html

    def save_report(self, scan_id: int, html_content: str) -> str:
        """Save report to disk and return URL path."""
        filename = f"report_{scan_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = settings.REPORTS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return f"/reports/{filename}"


report_service = ReportService()
