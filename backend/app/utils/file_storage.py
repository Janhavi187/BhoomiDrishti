"""File storage utilities for uploaded images."""
import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings


async def save_upload(file: UploadFile) -> dict:
    """Save uploaded file and return path info."""
    ext = file.filename.split(".")[-1].lower() if file.filename else "jpg"
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise ValueError(f"File type .{ext} not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}")

    unique_name = f"{uuid.uuid4().hex}.{ext}"
    file_path = settings.UPLOAD_DIR / unique_name

    with open(file_path, "wb") as buffer:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise ValueError(f"File too large. Max size: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB")
        buffer.write(content)

    return {
        "filename": unique_name,
        "original_name": file.filename,
        "path": str(file_path),
        "size": len(content),
    }


def get_image_url(filename: str) -> str:
    """Get the URL for an uploaded image."""
    return f"/uploads/{filename}"


def delete_upload(filename: str) -> bool:
    """Delete an uploaded file."""
    file_path = settings.UPLOAD_DIR / filename
    if file_path.exists():
        os.remove(file_path)
        return True
    return False
