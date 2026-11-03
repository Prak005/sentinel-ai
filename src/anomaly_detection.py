
from pathlib import Path
import joblib
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)


def train_isolation_forest(
    X_train,
    y_train,
    X_test,
    y_test,
    normal_label="BENIGN",
    model_path="models/isolation_forest.pkl"
):
    """
    Train Isolation Forest using only normal network traffic.
    """

    # Identify normal records in training data
    normal_mask = (
        y_train.astype(str).to_numpy() == normal_label
    )

    X_train_normal = X_train[normal_mask]

    if X_train_normal.shape[0] < 2:
        raise ValueError(
            "Not enough normal samples to train Isolation Forest."
        )

    # Initialize Isolation Forest
    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )

    # Train only on normal traffic
    print("Training Isolation Forest on BENIGN traffic...")

    model.fit(X_train_normal)

    # Predict on test data
    # 1 = normal, -1 = anomaly
    raw_predictions = model.predict(X_test)

    predicted_anomalies = (
        raw_predictions == -1
    ).astype(int)

    # Actual labels: 0 = normal, 1 = attack
    actual_anomalies = (
        y_test.astype(str).to_numpy() != normal_label
    ).astype(int)

    # Calculate anomaly scores
    # Lower scores indicate more unusual traffic
    anomaly_scores = model.decision_function(X_test)

    # Evaluation
    print("\nIsolation Forest Evaluation")
    print("-------------------------------")

    print(
        f"Accuracy:  {accuracy_score(actual_anomalies, predicted_anomalies):.4f}"
    )

    print(
        f"Precision: {precision_score(actual_anomalies, predicted_anomalies, zero_division=0):.4f}"
    )

    print(
        f"Recall:    {recall_score(actual_anomalies, predicted_anomalies, zero_division=0):.4f}"
    )

    print(
        f"F1 Score:  {f1_score(actual_anomalies, predicted_anomalies, zero_division=0):.4f}"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            actual_anomalies,
            predicted_anomalies,
            labels=[0, 1],
            target_names=["Normal", "Anomaly"],
            zero_division=0
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            actual_anomalies,
            predicted_anomalies,
            labels=[0, 1]
        )
    )

    # Save model
    Path(model_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(model, model_path)

    print(f"\nIsolation Forest saved: {model_path}")

    return model, predicted_anomalies, anomaly_scores
