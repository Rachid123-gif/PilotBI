"""
JWT verification utilities.

Supports both legacy HS256 (shared secret) and modern ES256/RS256
(asymmetric via Supabase JWKS endpoint). Newer Supabase projects
issue ES256 tokens by default.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

import httpx
from jose import JWTError, jwt

from app.config import get_settings

logger = logging.getLogger(__name__)

# In-memory JWKS cache to avoid hitting Supabase on every request.
_JWKS_CACHE: dict[str, Any] = {"keys": None, "fetched_at": 0.0}
_JWKS_TTL_SECONDS = 3600  # 1 hour


def _get_jwks() -> list[dict]:
    """Fetch and cache the JWKS from Supabase."""
    now = time.time()
    if _JWKS_CACHE["keys"] and (now - _JWKS_CACHE["fetched_at"]) < _JWKS_TTL_SECONDS:
        return _JWKS_CACHE["keys"]

    settings = get_settings()
    url = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        keys = data.get("keys", [])
        _JWKS_CACHE["keys"] = keys
        _JWKS_CACHE["fetched_at"] = now
        return keys
    except Exception as exc:
        logger.warning("Failed to fetch JWKS from %s: %s", url, exc)
        # Return any stale cache rather than nothing.
        return _JWKS_CACHE["keys"] or []


def _find_key_by_kid(keys: list[dict], kid: str) -> Optional[dict]:
    for key in keys:
        if key.get("kid") == kid:
            return key
    return None


def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Verify a Supabase JWT and return its payload.

    Handles both legacy HS256 tokens (shared secret) and modern
    asymmetric tokens (ES256, RS256) via the JWKS endpoint.

    Raises
    ------
    JWTError
        If the token is invalid, expired, or cannot be decoded.
    """
    settings = get_settings()

    try:
        header = jwt.get_unverified_header(token)
    except JWTError:
        logger.warning("JWT header parsing failed")
        raise

    alg = header.get("alg", "HS256")

    # Legacy shared-secret path
    if alg == "HS256":
        try:
            return jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
        except JWTError:
            logger.warning("HS256 JWT verification failed")
            raise

    # Asymmetric path (ES256, RS256, etc.) via JWKS
    kid = header.get("kid")
    if not kid:
        logger.warning("JWT missing 'kid' header for asymmetric verification")
        raise JWTError("JWT missing kid")

    keys = _get_jwks()
    key = _find_key_by_kid(keys, kid)

    # If the kid isn't in cache, force-refresh once (key rotation).
    if key is None:
        _JWKS_CACHE["fetched_at"] = 0.0
        keys = _get_jwks()
        key = _find_key_by_kid(keys, kid)

    if key is None:
        logger.warning("JWT kid %s not found in JWKS", kid)
        raise JWTError("Unknown signing key")

    try:
        return jwt.decode(
            token,
            key,
            algorithms=[alg],
            audience="authenticated",
        )
    except JWTError:
        logger.warning("%s JWT verification failed", alg)
        raise
