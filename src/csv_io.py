"""CSV loading and validation helpers for the Streamlit runtime."""
from __future__ import annotations

from typing import Any

import pandas as pd



def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with BOMs and surrounding whitespace removed from headers."""
    result = df.copy()
    result.columns = (
        result.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )
    if result.columns.duplicated().any():
        duplicates = result.columns[result.columns.duplicated()].unique().tolist()
        raise ValueError(
            "Duplicate column names after trimming whitespace: "
            + ", ".join(repr(name) for name in duplicates)
        )
    return result


def read_traffic_csv(uploaded_file: Any) -> pd.DataFrame:
    """Read a CSV upload with clear errors for common invalid-file cases.

    Upload size is enforced by Streamlit's file uploader (200 MB), not by a
    second, smaller application-level limit.
    """
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)

    try:
        frame = pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The uploaded file is empty or does not contain a CSV header.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError("The CSV could not be parsed. Check its delimiter, quoting, and row formatting.") from exc
    except UnicodeDecodeError as exc:
        raise ValueError("The CSV must use a supported text encoding, preferably UTF-8.") from exc

    if frame.empty:
        raise ValueError("The CSV contains column headers but no data rows.")
    if len(frame.columns) == 0:
        raise ValueError("The CSV does not contain any columns.")

    return normalize_column_names(frame)
