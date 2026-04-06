"""
File parsing utilities for CSV and Excel files.
"""

from __future__ import annotations

import io
import logging
import re
from typing import Optional, Union

import pandas as pd

logger = logging.getLogger(__name__)


def parse_file(data: Union[bytes, bytearray], file_type: str) -> pd.DataFrame:
    """
    Parse raw file bytes into a pandas DataFrame.

    Parameters
    ----------
    data : bytes
        Raw file content.
    file_type : str
        File extension: ``"csv"``, ``"xlsx"``, or ``"xls"``.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If the file cannot be parsed or is empty.
    """
    buf = io.BytesIO(data)

    try:
        if file_type == "csv":
            # Try common encodings and separators
            for encoding in ("utf-8", "latin-1", "cp1252"):
                for sep in (",", ";", "\t"):
                    try:
                        buf.seek(0)
                        df = pd.read_csv(buf, encoding=encoding, sep=sep)
                        if len(df.columns) > 1 or len(df) > 0:
                            logger.info(
                                "Parsed CSV: %d rows x %d cols (enc=%s, sep=%r)",
                                len(df), len(df.columns), encoding, sep,
                            )
                            return df
                    except Exception:
                        continue
            raise ValueError("Unable to parse CSV file with any encoding/separator combination")

        elif file_type in ("xlsx", "xls"):
            buf.seek(0)
            df = pd.read_excel(buf, engine="openpyxl" if file_type == "xlsx" else "xlrd")
            logger.info("Parsed Excel: %d rows x %d cols", len(df), len(df.columns))
            return df

        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Failed to parse file: {exc}") from exc


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a DataFrame:
    - Strip whitespace from string columns and column names
    - Remove completely empty rows
    - Try to parse date-like columns
    - Remove duplicate rows

    Returns a new DataFrame.
    """
    df = df.copy()

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]

    # Strip whitespace in string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": None, "None": None, "": None})

    # Remove rows where all values are null
    df = df.dropna(how="all")

    # Remove duplicates
    df = df.drop_duplicates()

    # Try to parse date columns
    for col in df.columns:
        col_lower = col.lower()
        if any(kw in col_lower for kw in ("date", "jour", "mois", "annee", "periode")):
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            except Exception:
                pass

    # Reset index
    df = df.reset_index(drop=True)

    logger.info("Cleaned DataFrame: %d rows x %d cols", len(df), len(df.columns))
    return df


def detect_date_column(df: pd.DataFrame) -> Optional[str]:
    """
    Find the most likely date column in the DataFrame.

    Strategy:
    1. Look for columns already parsed as datetime64
    2. Look for column names containing date-related keywords
    3. Try to parse each object column as dates

    Returns the column name or ``None``.
    """
    # Already datetime columns
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    if datetime_cols:
        return datetime_cols[0]

    # Keyword-based detection
    date_keywords = ("date", "jour", "mois", "periode", "timestamp", "created", "facture_date")
    for col in df.columns:
        col_lower = col.lower().strip()
        for kw in date_keywords:
            if kw in col_lower:
                # Verify it can be parsed
                try:
                    parsed = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
                    if parsed.notna().sum() > len(df) * 0.5:
                        return col
                except Exception:
                    continue

    # Brute-force: try each object column
    for col in df.select_dtypes(include=["object"]).columns:
        try:
            parsed = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            if parsed.notna().sum() > len(df) * 0.5:
                return col
        except Exception:
            continue

    return None
