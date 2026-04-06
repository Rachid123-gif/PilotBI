"""
JWT verification utilities.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from jose import JWTError, jwt

from app.config import get_settings

logger = logging.getLogger(__name__)


def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Verify a Supabase JWT and return its payload.

    Raises
    ------
    JWTError
        If the token is invalid, expired, or cannot be decoded.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except JWTError:
        logger.warning("JWT verification failed")
        raise
