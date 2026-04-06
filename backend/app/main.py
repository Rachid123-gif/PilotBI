"""
PilotBI FastAPI application entry point.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import admin, alerts, billing, dashboard, health, reports, upload, webhooks

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger("pilotbi")


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    logger.info("PilotBI backend starting up")
    # Eagerly validate settings so missing env vars fail fast
    get_settings()
    yield
    logger.info("PilotBI backend shutting down")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
app = FastAPI(
    title="PilotBI API",
    description="Business Intelligence SaaS API for Moroccan SMEs",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router, tags=["Health"])
app.include_router(upload.router, prefix="/v1", tags=["Upload"])
app.include_router(dashboard.router, prefix="/v1", tags=["Dashboard"])
app.include_router(reports.router, prefix="/v1", tags=["Reports"])
app.include_router(alerts.router, prefix="/v1", tags=["Alerts"])
app.include_router(billing.router, prefix="/v1", tags=["Billing"])
app.include_router(webhooks.router, prefix="/v1", tags=["Webhooks"])
app.include_router(admin.router, prefix="/v1", tags=["Admin"])
