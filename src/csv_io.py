"""Memory-conscious CSV loading and validation helpers for Streamlit."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PREPROCESSOR_PATH = BASE_DIR / "models" / "cicids2017" / "preprocessor_bundle.pkl"


@lru_cache(maxsize=1)
def _model_feature_columns() -> tuple[str, ...]:
    """Load only the small preprocessing bundle to obtain model input names.

    Loading the full model ensemble merely to infer CSV dtypes would waste RAM
    before the user starts analysis. The bundle contains the feature list and
    is tiny compared with the trained estimators.
    """
    if not PREPROCESSOR_PATH.exists():
        return ()
    bundle = joblib.load(PREPROCESSOR_PATH)
    return tuple(str(column) for column in bundle.get("feature_columns", ()))


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize headers in place to avoid copying a large DataFrame."""
    normalized = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )
    if normalized.duplicated().any():
        duplicates = normalized[normalized.duplicated()].unique().tolist()
        raise ValueError(
            "Duplicate column names after trimming whitespace: "
            + ", ".join(repr(name) for name in duplicates)
        )
    df.columns = normalized
    return df


def read_traffic_csv(uploaded_file: Any) -> pd.DataFrame:
    """Read a compatible traffic CSV using float32 for model features.

    The Streamlit uploader remains configured for 200 MB. Numeric model
    features are parsed directly as float32, avoiding the large temporary
    float64 DataFrame followed by a second downcast copy.
    """
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)

    try:
        # Read only the header first so dtype hints still apply when CSV
        # headers contain a BOM or surrounding whitespace.
        header = pd.read_csv(uploaded_file, nrows=0)
        feature_columns = set(_model_feature_columns())
        dtype_map = {
            raw_name: "float32"
            for raw_name in header.columns
            if str(raw_name).replace("\ufeff", "").strip() in feature_columns
        }
        uploaded_file.seek(0)

        frame = pd.read_csv(
            uploaded_file,
            dtype=dtype_map or None,
            low_memory=True,
        )
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The uploaded file is empty or does not contain a CSV header.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(
            "The CSV could not be parsed. Check its delimiter, quoting, and row formatting."
        ) from exc
    except UnicodeDecodeError as exc:
        raise ValueError(
            "The CSV must use a supported text encoding, preferably UTF-8."
        ) from exc
    except (TypeError, ValueError) as exc:
        # Keep the error user-facing if a feature column contains non-numeric
        # text; the model pipeline cannot use such values without coercion.
        raise ValueError(
            "One or more model feature columns contain non-numeric values. "
            "Please check that the uploaded file is a compatible network-flow CSV."
        ) from exc

    if frame.empty:
        raise ValueError("The CSV contains column headers but no data rows.")
    if len(frame.columns) == 0:
        raise ValueError("The CSV does not contain any columns.")

    return normalize_column_names(frame)
