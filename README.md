# Sentinel AI

Streamlit dashboard for network intrusion detection using the existing trained Random Forest and Isolation Forest models. The refactor and runtime safeguards do not retrain or alter the model artifacts or hybrid risk-classification rules.

## Run locally

Use the Python virtual environment from this project directory. On Arch Linux with Fish:

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `.venv` already exists and works, do not recreate it unnecessarily. If you moved the project directory and the environment points to the old path, recreate `.venv` and reinstall dependencies. Run the app from this project root so the runtime artifacts resolve under `models/cicids2017/`.

The `.venv/` directory is local-only and should not be committed or included in project archives.

## Structure

- `app.py`: Streamlit setup, custom sidebar navigation, and page routing.
- `views/`: six manually routed dashboard pages.
- `ui/styles.py`: dashboard CSS.
- `ui/components.py`: reusable UI components.
- `src/inference.py`: runtime inference pipeline; loads trained artifacts once per process and preserves the existing hybrid decisions and calibrated risk thresholds.
- `src/csv_io.py`: CSV parsing and header validation.
- `models/cicids2017/`: runtime model artifacts and calibrated risk thresholds.
- `tests/`: unit tests for CSV validation, model-loading cache, and hybrid inference behavior.

Training and offline model scripts are not part of the runtime refactor.

## Runtime safeguards

- CSV uploads retain the 200 MB Streamlit limit. No additional 50 MiB application-level limit is applied. Uploaded files are checked for empty content, malformed rows, unsupported text encoding, and duplicate headers after normalization.
- Missing model artifacts and invalid/missing features produce actionable validation errors.
- Unexpected UI inference errors are logged to the terminal while the dashboard displays a less noisy message.
- Inference model artifacts are cached in-process to avoid loading all pickle files on every prediction. If model files are replaced while the app is running, restart Streamlit or call `load_models.cache_clear()` before loading the new artifacts.
- Analysis results are tied to the uploaded file's content hash, preventing a different file with the same filename and size from showing stale results.

## Tests

Install the development dependencies and run the tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests use fake estimators for prediction-rule checks, so they do not require retraining or depend on the actual serialized model files.

## Model-version compatibility

Serialized scikit-learn estimators should be loaded with the compatible scikit-learn version used when they were created. Check the environment used for training before changing the pinned dependency. Do not retrain or replace the saved model files merely to resolve a dependency warning without first validating the required version.
