"""
Data source upload and management endpoints.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, status
from supabase import Client

from app.dependencies import get_supabase_client, require_organization
from app.models.enums import DataSourceStatus, DataSourceType
from app.models.schemas import (
    ColumnMappingUpdate,
    DataSourceList,
    DataSourceResponse,
    UploadResponse,
)
from app.services.column_detector import detect_columns
from app.services.file_parser import clean_dataframe, detect_date_column, parse_file
from app.utils.storage import delete_file, upload_file

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_EXTENSIONS = {
    "csv": DataSourceType.CSV,
    "xlsx": DataSourceType.EXCEL,
    "xls": DataSourceType.EXCEL,
}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


# ---------------------------------------------------------------------------
# Background task: process an uploaded file
# ---------------------------------------------------------------------------

async def _process_upload(source_id: str, bucket: str, storage_path: str, file_type: str, db: Client):
    """Parse the uploaded file, detect columns, store rows."""
    try:
        # Update status -> processing
        db.table("data_sources").update({"status": DataSourceStatus.PROCESSING.value}).eq("id", source_id).execute()

        # Download from storage
        from app.utils.storage import download_file
        raw = await download_file(bucket, storage_path)

        # Parse
        df = parse_file(raw, file_type)
        df = clean_dataframe(df)

        # Detect columns
        mappings = detect_columns(df)
        date_col = detect_date_column(df)

        # Build column_mappings JSON
        mapping_list = []
        for col in df.columns:
            mapping_list.append({
                "original_name": col,
                "mapped_name": mappings.get(col),
                "kpi_type": mappings.get(col),
                "detected": col in mappings,
            })

        # Store rows in data_rows table
        org_result = db.table("data_sources").select("organization_id").eq("id", source_id).single().execute()
        org_id = org_result.data["organization_id"]

        rows_to_insert = []
        for _, row in df.iterrows():
            row_data = {}
            for col in df.columns:
                mapped = mappings.get(col, col)
                val = row[col]
                # Convert numpy types to native Python
                if hasattr(val, "item"):
                    val = val.item()
                if isinstance(val, float) and val != val:  # NaN check
                    val = None
                row_data[mapped] = val

            rows_to_insert.append({
                "id": str(uuid.uuid4()),
                "data_source_id": source_id,
                "organization_id": org_id,
                "row_data": row_data,
                "date_value": str(row[date_col]) if date_col and date_col in row.index else None,
            })

        # Batch insert (chunks of 500)
        for i in range(0, len(rows_to_insert), 500):
            chunk = rows_to_insert[i : i + 500]
            db.table("data_rows").insert(chunk).execute()

        # Update source as ready
        db.table("data_sources").update({
            "status": DataSourceStatus.READY.value,
            "row_count": len(rows_to_insert),
            "column_mappings": mapping_list,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", source_id).execute()

        logger.info("Processed source %s: %d rows", source_id, len(rows_to_insert))

    except Exception as exc:
        logger.exception("Failed to process source %s", source_id)
        db.table("data_sources").update({
            "status": DataSourceStatus.ERROR.value,
            "error_message": str(exc)[:500],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", source_id).execute()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_data_source(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Upload a CSV or Excel file as a new data source."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 50 MB limit")

    file_type = ALLOWED_EXTENSIONS[ext]
    source_id = str(uuid.uuid4())
    org_id = user["organization_id"]
    storage_path = f"{org_id}/{source_id}/{file.filename}"
    bucket = "uploads"

    # Upload to storage
    await upload_file(bucket, storage_path, content)

    # Insert data_source row
    now = datetime.now(timezone.utc).isoformat()
    db.table("data_sources").insert({
        "id": source_id,
        "organization_id": org_id,
        "filename": file.filename,
        "file_type": file_type.value,
        "storage_path": storage_path,
        "status": DataSourceStatus.PENDING.value,
        "created_at": now,
        "updated_at": now,
        "uploaded_by": user["id"],
    }).execute()

    # Trigger background processing
    background_tasks.add_task(_process_upload, source_id, bucket, storage_path, ext, db)

    return UploadResponse(
        id=source_id,
        filename=file.filename,
        file_type=file_type,
        status=DataSourceStatus.PENDING,
        created_at=datetime.now(timezone.utc),
    )


@router.get("/sources", response_model=DataSourceList)
async def list_sources(
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """List all data sources for the user's organization."""
    result = (
        db.table("data_sources")
        .select("*")
        .eq("organization_id", user["organization_id"])
        .order("created_at", desc=True)
        .execute()
    )
    items = result.data or []
    return DataSourceList(items=items, total=len(items))


@router.get("/sources/{source_id}", response_model=DataSourceResponse)
async def get_source(
    source_id: str,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Get a single data source with its column mappings."""
    result = (
        db.table("data_sources")
        .select("*")
        .eq("id", source_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Data source not found")
    return result.data


@router.put("/sources/{source_id}/mapping", response_model=DataSourceResponse)
async def update_mapping(
    source_id: str,
    body: ColumnMappingUpdate,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Update column mappings for a data source."""
    # Verify ownership
    existing = (
        db.table("data_sources")
        .select("id")
        .eq("id", source_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Data source not found")

    mappings_json = [m.model_dump() for m in body.mappings]
    result = (
        db.table("data_sources")
        .update({
            "column_mappings": mappings_json,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })
        .eq("id", source_id)
        .execute()
    )
    return result.data[0] if result.data else existing.data


@router.post("/sources/{source_id}/sync", status_code=status.HTTP_202_ACCEPTED)
async def sync_source(
    source_id: str,
    background_tasks: BackgroundTasks,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Re-trigger processing for a data source."""
    existing = (
        db.table("data_sources")
        .select("storage_path, file_type")
        .eq("id", source_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Data source not found")

    # Delete existing rows
    db.table("data_rows").delete().eq("data_source_id", source_id).execute()

    storage_path = existing.data["storage_path"]
    file_type = existing.data["file_type"]
    ext = "csv" if file_type == "csv" else "xlsx"

    background_tasks.add_task(_process_upload, source_id, "uploads", storage_path, ext, db)
    return {"detail": "Sync triggered", "source_id": source_id}


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: str,
    user=Depends(require_organization),
    db: Client = Depends(get_supabase_client),
):
    """Delete a data source and all its data."""
    existing = (
        db.table("data_sources")
        .select("storage_path")
        .eq("id", source_id)
        .eq("organization_id", user["organization_id"])
        .maybe_single()
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Data source not found")

    # Delete rows
    db.table("data_rows").delete().eq("data_source_id", source_id).execute()

    # Delete from storage
    storage_path = existing.data.get("storage_path")
    if storage_path:
        try:
            await delete_file("uploads", storage_path)
        except Exception:
            logger.warning("Could not delete storage file %s", storage_path)

    # Delete source record
    db.table("data_sources").delete().eq("id", source_id).execute()
