from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    f1_score
)


# --------------------------------------------------
# 1. PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "processed" / "test.csv"
MODEL_DIR = BASE_DIR / "models" / "cicids2017"

CHUNK_SIZE = 10_000


# --------------------------------------------------
# 2. LOAD TRAINED MODELS
# --------------------------------------------------

print("\nSENTINEL AI - MODEL EVALUATION")
print("=" * 65)

print("\nLoading trained models...")

print("\nLoading trained models...")

rf_model = joblib.load(
    MODEL_DIR / "random_forest.pkl"
)

if_model = joblib.load(
    MODEL_DIR / "isolation_forest.pkl"
)

bundle = joblib.load(
    MODEL_DIR / "preprocessor_bundle.pkl"
)

# Disable parallel prediction for stable execution
rf_model.set_params(n_jobs=1, verbose=0)
if_model.set_params(n_jobs=1)

rf_imputer = bundle["rf_imputer"]
if_imputer = bundle["if_imputer"]
feature_columns = bundle["feature_columns"]

class_labels = [str(label) for label in rf_model.classes_]

print("Models loaded successfully!")
print(f"Features: {len(feature_columns)}")
print(f"Classes: {len(class_labels)}")


# --------------------------------------------------
# 3. PREPARE CHUNKED TEST DATA READER
# --------------------------------------------------

raw_columns = pd.read_csv(
    DATA_PATH,
    nrows=0
).columns.tolist()

clean_columns = [
    str(col).strip() for col in raw_columns
]

if len(set(clean_columns)) != len(clean_columns):
    raise ValueError("Duplicate columns found in test dataset.")

dtype_map = {}

for raw_col, clean_col in zip(raw_columns, clean_columns):

    if clean_col == "Label":
        dtype_map[raw_col] = "category"

    elif clean_col == "Group_ID":
        dtype_map[raw_col] = "uint64"

    else:
        dtype_map[raw_col] = np.float32


reader = pd.read_csv(
    DATA_PATH,
    dtype=dtype_map,
    chunksize=CHUNK_SIZE,
    low_memory=False
)


# --------------------------------------------------
# 4. COLLECT PREDICTIONS
# --------------------------------------------------

y_true_parts = []
rf_prediction_parts = []
if_prediction_parts = []
hybrid_prediction_parts = []

total_records = 0

print("\nProcessing held-out test dataset...")

for chunk_number, chunk in enumerate(reader, start=1):

    chunk.columns = clean_columns

    missing_columns = [
        col for col in feature_columns
        if col not in chunk.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing test features: {missing_columns}"
        )

    X = chunk.loc[:, feature_columns].copy()

    X.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    y_true = chunk["Label"].astype(str).to_numpy()

    unknown_labels = set(np.unique(y_true)) - set(class_labels)

    if unknown_labels:
        raise ValueError(
            f"Unknown test labels: {unknown_labels}"
        )

    # Apply separate trained imputers
    X_rf = rf_imputer.transform(X)
    X_if = if_imputer.transform(X)

    # Random Forest predictions
    rf_predictions = rf_model.predict(X_rf)

    # Isolation Forest predictions
    if_predictions = if_model.predict(X_if)

    # Convert IF output into binary labels:
    # 1 = Attack / Anomaly
    # 0 = BENIGN / Normal

    if_binary = (if_predictions == -1).astype(np.int8)

    # Hybrid detection:
    # RF attack OR IF anomaly = detected attack
    hybrid_binary = (
        (rf_predictions != "BENIGN") |
        (if_predictions == -1)
    ).astype(np.int8)

    y_true_parts.append(y_true)
    rf_prediction_parts.append(rf_predictions)
    if_prediction_parts.append(if_binary)
    hybrid_prediction_parts.append(hybrid_binary)

    total_records += len(chunk)

    print(
        f"Processed chunk {chunk_number} | "
        f"Total records: {total_records:,}"
    )


# --------------------------------------------------
# 5. COMBINE RESULTS
# --------------------------------------------------

y_true_all = np.concatenate(y_true_parts)

rf_pred_all = np.concatenate(rf_prediction_parts)

if_pred_all = np.concatenate(if_prediction_parts)

hybrid_pred_all = np.concatenate(hybrid_prediction_parts)

y_true_binary = (
    y_true_all != "BENIGN"
).astype(np.int8)

print("\nTest dataset processing completed!")
print(f"Total test records: {len(y_true_all):,}")


# --------------------------------------------------
# 6. RANDOM FOREST EVALUATION
# --------------------------------------------------

print("\n" + "=" * 65)
print("RANDOM FOREST - MULTICLASS EVALUATION")
print("=" * 65)

rf_accuracy = accuracy_score(
    y_true_all,
    rf_pred_all
)

rf_weighted_precision, rf_weighted_recall, rf_weighted_f1, _ = (
    precision_recall_fscore_support(
        y_true_all,
        rf_pred_all,
        average="weighted",
        zero_division=0
    )
)

rf_macro_f1 = f1_score(
    y_true_all,
    rf_pred_all,
    average="macro",
    zero_division=0
)

rf_report = classification_report(
    y_true_all,
    rf_pred_all,
    labels=class_labels,
    target_names=class_labels,
    zero_division=0,
    digits=4
)

rf_cm = confusion_matrix(
    y_true_all,
    rf_pred_all,
    labels=class_labels
)

print(f"\nAccuracy:          {rf_accuracy:.4f}")
print(f"Weighted Precision: {rf_weighted_precision:.4f}")
print(f"Weighted Recall:    {rf_weighted_recall:.4f}")
print(f"Weighted F1:        {rf_weighted_f1:.4f}")
print(f"Macro F1:           {rf_macro_f1:.4f}")

print("\nClassification Report:")
print(rf_report)

print("\nConfusion Matrix:")
print(rf_cm)


# --------------------------------------------------
# 7. BINARY EVALUATION HELPER
# --------------------------------------------------

def evaluate_binary_model(name, y_true, y_pred):

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    )

    tn, fp, fn, tp = cm.ravel()

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            y_true,
            y_pred,
            average="binary",
            zero_division=0
        )
    )

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0
    )

    report = classification_report(
        y_true,
        y_pred,
        labels=[0, 1],
        target_names=["BENIGN", "ATTACK"],
        zero_division=0,
        digits=4
    )

    print("\n" + "=" * 65)
    print(name)
    print("=" * 65)

    print(f"\nAccuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"FPR:       {fpr:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(report)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "fpr": fpr,
        "confusion_matrix": cm,
        "report": report
    }


# --------------------------------------------------
# 8. ISOLATION FOREST EVALUATION
# --------------------------------------------------

if_results = evaluate_binary_model(
    "ISOLATION FOREST - ANOMALY DETECTION",
    y_true_binary,
    if_pred_all
)


# --------------------------------------------------
# 9. HYBRID DETECTION EVALUATION
# --------------------------------------------------

hybrid_results = evaluate_binary_model(
    "SENTINEL AI - HYBRID DETECTION",
    y_true_binary,
    hybrid_pred_all
)


# --------------------------------------------------
# 10. HYBRID STATUS DISTRIBUTION
# --------------------------------------------------

known_attacks = int(
    np.sum(rf_pred_all != "BENIGN")
)

suspicious_anomalies = int(
    np.sum(
        (rf_pred_all == "BENIGN") &
        (if_pred_all == 1)
    )
)

normal_flows = int(
    np.sum(hybrid_pred_all == 0)
)

print("\n" + "=" * 65)
print("HYBRID DETECTION STATUS DISTRIBUTION")
print("=" * 65)

print(f"Total test flows:       {len(y_true_all):,}")
print(f"Known attacks:          {known_attacks:,}")
print(f"Suspicious anomalies:   {suspicious_anomalies:,}")
print(f"Normal traffic:         {normal_flows:,}")


# --------------------------------------------------
# 11. SAVE EVALUATION REPORT
# --------------------------------------------------

report_text = f"""
SENTINEL AI - CIC-IDS2017 EVALUATION REPORT

Total test records: {len(y_true_all):,}

RANDOM FOREST
Accuracy: {rf_accuracy:.4f}
Weighted Precision: {rf_weighted_precision:.4f}
Weighted Recall: {rf_weighted_recall:.4f}
Weighted F1: {rf_weighted_f1:.4f}
Macro F1: {rf_macro_f1:.4f}

Classification Report:
{rf_report}

Confusion Matrix:
{rf_cm}

ISOLATION FOREST
Accuracy: {if_results['accuracy']:.4f}
Precision: {if_results['precision']:.4f}
Recall: {if_results['recall']:.4f}
F1: {if_results['f1']:.4f}
False Positive Rate: {if_results['fpr']:.4f}

Confusion Matrix:
{if_results['confusion_matrix']}

HYBRID DETECTION
Accuracy: {hybrid_results['accuracy']:.4f}
Precision: {hybrid_results['precision']:.4f}
Recall: {hybrid_results['recall']:.4f}
F1: {hybrid_results['f1']:.4f}
False Positive Rate: {hybrid_results['fpr']:.4f}

Confusion Matrix:
{hybrid_results['confusion_matrix']}

HYBRID STATUS DISTRIBUTION
Known attacks: {known_attacks}
Suspicious anomalies: {suspicious_anomalies}
Normal traffic: {normal_flows}
"""

report_path = MODEL_DIR / "evaluation_report.txt"

report_path.write_text(
    report_text,
    encoding="utf-8"
)

print("\nEvaluation report saved to:")
print(report_path)

print("\nMODEL EVALUATION COMPLETED!")