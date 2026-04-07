"""
PilotBI application configuration.
Loads settings from environment variables. Optional services have defaults.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ---------- Supabase (required) ----------
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str

    # ---------- Anthropic (optional — needed for AI reports) ----------
    ANTHROPIC_API_KEY: str = ""

    # ---------- Stripe (optional — needed for billing) ----------
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_STARTER_MONTHLY: str = ""
    STRIPE_PRICE_STARTER_ANNUAL: str = ""
    STRIPE_PRICE_PRO_MONTHLY: str = ""
    STRIPE_PRICE_PRO_ANNUAL: str = ""
    STRIPE_PRICE_EQUIPE_MONTHLY: str = ""
    STRIPE_PRICE_EQUIPE_ANNUAL: str = ""

    # ---------- Resend (optional — needed for email alerts) ----------
    RESEND_API_KEY: str = ""
    RESEND_FROM_EMAIL: str = "PilotBI <noreply@pilotbi.com>"

    # ---------- Twilio (optional — needed for WhatsApp alerts) ----------
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_FROM: str = ""

    # ---------- CORS ----------
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def stripe_price_map(self) -> dict[str, str]:
        """Map plan+interval keys to Stripe price IDs."""
        return {
            "starter_monthly": self.STRIPE_PRICE_STARTER_MONTHLY,
            "starter_annual": self.STRIPE_PRICE_STARTER_ANNUAL,
            "pro_monthly": self.STRIPE_PRICE_PRO_MONTHLY,
            "pro_annual": self.STRIPE_PRICE_PRO_ANNUAL,
            "equipe_monthly": self.STRIPE_PRICE_EQUIPE_MONTHLY,
            "equipe_annual": self.STRIPE_PRICE_EQUIPE_ANNUAL,
        }

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()  # type: ignore[call-arg]
