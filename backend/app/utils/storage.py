"""
Supabase Storage helper functions.
"""

from __future__ import annotations

import logging
from typing import Union

from supabase import Client

from app.config import get_settings
from app.dependencies import _build_supabase_client

logger = logging.getLogger(__name__)


def _get_client() -> Client:
    """Return a service-role Supabase client for storage operations."""
    return _build_supabase_client()


async def upload_file(bucket: str, path: str, data: Union[bytes, bytearray]) -> str:
    """
    Upload a file to Supabase Storage.

    Parameters
    ----------
    bucket : str
        The storage bucket name (e.g. ``"uploads"``).
    path : str
        The destination path inside the bucket.
    data : bytes
        Raw file content.

    Returns
    -------
    str
        The full storage path ``bucket/path``.
    """
    client = _get_client()
    try:
        client.storage.from_(bucket).upload(
            path=path,
            file=data,
            file_options={"content-type": "application/octet-stream"},
        )
        logger.info("Uploaded %s/%s (%d bytes)", bucket, path, len(data))
        return f"{bucket}/{path}"
    except Exception:
        logger.exception("Failed to upload %s/%s", bucket, path)
        raise


async def download_file(bucket: str, path: str) -> bytes:
    """
    Download a file from Supabase Storage.

    Returns
    -------
    bytes
        The raw file content.
    """
    client = _get_client()
    try:
        response = client.storage.from_(bucket).download(path)
        logger.info("Downloaded %s/%s", bucket, path)
        return response
    except Exception:
        logger.exception("Failed to download %s/%s", bucket, path)
        raise


async def delete_file(bucket: str, path: str) -> None:
    """Delete a file from Supabase Storage."""
    client = _get_client()
    try:
        client.storage.from_(bucket).remove([path])
        logger.info("Deleted %s/%s", bucket, path)
    except Exception:
        logger.exception("Failed to delete %s/%s", bucket, path)
        raise
