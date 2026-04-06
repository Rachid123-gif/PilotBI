"""
FastAPI dependency injection functions.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from supabase import Client, create_client

from app.config import Settings, get_settings
from app.utils.auth import verify_jwt

logger = logging.getLogger(__name__)

_bearer_scheme = HTTPBearer()

# ---------------------------------------------------------------------------
# Supabase client
# ---------------------------------------------------------------------------

_supabase_client: Client | None = None


def _build_supabase_client() -> Client:
    """Build a Supabase client using service-role key (server-side only)."""
    settings = get_settings()
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def get_supabase_client() -> Client:
    """FastAPI dependency that returns a Supabase service-role client."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = _build_supabase_client()
    return _supabase_client


# ---------------------------------------------------------------------------
# Current user
# ---------------------------------------------------------------------------

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Client = Depends(get_supabase_client),
) -> Dict[str, Any]:
    """
    Validate the JWT from the ``Authorization: Bearer <token>`` header and
    return a user dict with ``id``, ``email``, and ``organization_id``.

    Raises ``401`` if the token is missing / invalid and ``403`` if the user
    has no organization yet.
    """
    try:
        payload = verify_jwt(credentials.credentials)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    email: str | None = payload.get("email")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing subject",
        )

    # Fetch organization membership from the profiles table
    result = (
        db.table("profiles")
        .select("organization_id")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )

    organization_id: str | None = None
    if result.data:
        organization_id = result.data.get("organization_id")

    return {
        "id": user_id,
        "email": email,
        "organization_id": organization_id,
    }


def require_organization(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Dependency that ensures the user belongs to an organization."""
    if not user.get("organization_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not part of any organization. Complete onboarding first.",
        )
    return user


def require_admin(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Dependency that ensures the user has admin role."""
    # Admin role is stored in JWT app_metadata by Supabase
    # For service-level admin check we verify against the profiles table
    db = get_supabase_client()
    result = (
        db.table("profiles")
        .select("role")
        .eq("id", user["id"])
        .maybe_single()
        .execute()
    )
    if not result.data or result.data.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
