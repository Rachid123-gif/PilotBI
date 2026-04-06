"""
Health-check endpoint.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Return service health status."""
    return {"status": "ok", "version": "1.0.0"}
