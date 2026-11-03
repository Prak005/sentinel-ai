import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import src.inference as inference


class FakeImputer:
    def transform(self, frame):
        return frame.to_numpy(dtype=float)


class FakeRandomForest:
    def __init__(self, labels):
        self.labels = np.asarray(labels)
        self.params = {}

    def set_params(self, **kwargs):
        self.params.update(kwargs)
        return self

    def predict(self, values):
        return self.labels[: len(values)]


class FakeIsolationForest:
    def __init__(self, labels, scores):
        self.labels = np.asarray(labels)
        self.scores = np.asarray(scores, dtype=float)
        self.params = {}

    def set_params(self, **kwargs):
        self.params.update(kwargs)
        return self

    def predict(self, values):
        return self.labels[: len(values)]

    def decision_function(self, values):
        return self.scores[: len(values)]


def fake_models(rf_labels, if_labels, scores):
    return (
        FakeRandomForest(rf_labels),
        FakeIsolationForest(if_labels, scores),
        FakeImputer(),
        FakeImputer(),
        ["f1", "f2"],
        -0.4,
        0.0,
    )


def test_predict_traffic_preserves_hybrid_status_and_risk_rules(monkeypatch):
    monkeypatch.setattr(
        inference,
        "load_models",
        lambda: fake_models(
            ["BENIGN", "DoS", "BENIGN"],
            [-1, 1, -1],
            [-0.5, -0.2, -0.05],
        ),
    )
    frame = pd.DataFrame({" f1 ": [1, 2, 3], "f2": [4, 5, 6], "Label": ["x"] * 3})

    result = inference.predict_traffic(frame)

    assert result["Final Status"].tolist() == [
        "Suspicious Anomaly", "Known Attack", "Suspicious Anomaly"
    ]
    assert result["Risk Level"].tolist() == ["HIGH RISK", "CONFIRMED ATTACK", "MEDIUM RISK"]
    assert result["IF Prediction"].tolist() == ["Anomaly", "Normal", "Anomaly"]
    assert result["Anomaly Score"].tolist() == [-0.5, -0.2, -0.05]


def test_predict_traffic_rejects_empty_frame(monkeypatch):
    monkeypatch.setattr(inference, "load_models", lambda: pytest.fail("models should not load"))
    with pytest.raises(ValueError, match="empty"):
        inference.predict_traffic(pd.DataFrame())


def test_predict_traffic_rejects_missing_features(monkeypatch):
    monkeypatch.setattr(inference, "load_models", lambda: fake_models(["BENIGN"], [1], [0.1]))
    with pytest.raises(ValueError, match="Missing required columns"):
        inference.predict_traffic(pd.DataFrame({"f1": [1]}))


def test_predict_traffic_rejects_duplicate_normalized_columns(monkeypatch):
    monkeypatch.setattr(inference, "load_models", lambda: fake_models(["BENIGN"], [1], [0.1]))
    frame = pd.DataFrame([[1, 2]], columns=["f1", " f1 "])
    with pytest.raises(ValueError, match="Duplicate columns"):
        inference.predict_traffic(frame)


def test_load_models_caches_loaded_artifacts(monkeypatch, tmp_path):
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    for name in ("random_forest.pkl", "isolation_forest.pkl", "preprocessor_bundle.pkl"):
        (model_dir / name).touch()
    (model_dir / "risk_thresholds.json").write_text(
        json.dumps({"high_risk_max_score": -0.4, "medium_risk_max_score": 0.0}),
        encoding="utf-8",
    )

    rf = FakeRandomForest([])
    isolation = FakeIsolationForest([], [])
    bundle = {"rf_imputer": FakeImputer(), "if_imputer": FakeImputer(), "feature_columns": ["f1", "f2"]}
    calls = []

    def fake_joblib_load(path):
        calls.append(Path(path).name)
        if Path(path).name == "random_forest.pkl":
            return rf
        if Path(path).name == "isolation_forest.pkl":
            return isolation
        return bundle

    monkeypatch.setattr(inference, "MODEL_DIR", model_dir)
    monkeypatch.setattr(inference.joblib, "load", fake_joblib_load)
    inference.load_models.cache_clear()
    try:
        first = inference.load_models()
        second = inference.load_models()
        assert first is second
        assert len(calls) == 3
    finally:
        inference.load_models.cache_clear()


def test_predict_traffic_processes_rows_in_bounded_batches(monkeypatch):
    class BatchRandomForest(FakeRandomForest):
        def __init__(self):
            super().__init__([])
            self.max_batch = 0

        def predict(self, values):
            self.max_batch = max(self.max_batch, len(values))
            return np.where(values[:, 0] >= 4, "DoS", "BENIGN")

    class BatchIsolationForest(FakeIsolationForest):
        def __init__(self):
            super().__init__([], [])
            self.max_batch = 0

        def predict(self, values):
            self.max_batch = max(self.max_batch, len(values))
            return np.where(values[:, 0] >= 3, -1, 1)

        def decision_function(self, values):
            return values[:, 0] / 10.0 - 0.5

    rf = BatchRandomForest()
    isolation = BatchIsolationForest()
    monkeypatch.setattr(
        inference,
        "load_models",
        lambda: (rf, isolation, FakeImputer(), FakeImputer(), ["f1", "f2"], -0.4, 0.0),
    )

    frame = pd.DataFrame({"f1": [1, 2, 3, 4, 5], "f2": [0, 0, 0, 0, 0]})
    result = inference.predict_traffic(frame, batch_size=2)

    assert len(result) == 5
    assert rf.max_batch <= 2
    assert isolation.max_batch <= 2
    assert result["Final Status"].tolist() == [
        "Normal", "Normal", "Suspicious Anomaly", "Known Attack", "Known Attack"
    ]
