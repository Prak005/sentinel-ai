
import pandas as pd


def detect_intrusions(
    X,
    random_forest_model,
    isolation_forest_model,
    normal_label="BENIGN"
):
    """
    Combine Random Forest and Isolation Forest predictions.
    """

    # Random Forest predictions
    rf_predictions = random_forest_model.predict(X)

    # Isolation Forest predictions
    # 1 = Normal, -1 = Anomaly
    if_predictions = isolation_forest_model.predict(X)

    # Get anomaly scores
    anomaly_scores = isolation_forest_model.decision_function(X)

    results = []

    for rf_label, if_label, score in zip(
        rf_predictions,
        if_predictions,
        anomaly_scores
    ):

        # Hybrid decision logic
        if rf_label != normal_label:
            status = "Known Attack"

        elif if_label == -1:
            status = "Suspicious Anomaly"

        else:
            status = "Normal"

        results.append({
            "RF Prediction": rf_label,
            "IF Prediction": (
                "Anomaly" if if_label == -1 else "Normal"
            ),
            "Anomaly Score": round(float(score), 4),
            "Final Status": status
        })

    return pd.DataFrame(results)
