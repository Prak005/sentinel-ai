from pathlib import Path
import gc
import numpy as np
import pandas as pd
import joblib

from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, IsolationForest


BASE_DIR = Path(__file__).resolve().parent
TRAIN_PATH = BASE_DIR / "data" / "processed" / "train_model.csv"
MODEL_DIR = BASE_DIR / "models" / "cicids2017"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

RF_SAMPLE_SIZE = 500_000
IF_SAMPLE_SIZE = 100_000
RANDOM_STATE = 42


def load_training_data(path):

    raw_columns = pd.read_csv(path, nrows=0).columns.tolist()
    clean_columns = [str(col).strip() for col in raw_columns]

    if len(set(clean_columns)) != len(clean_columns):
        raise ValueError("Duplicate columns found after stripping spaces.")

    dtype_map = {}

    for raw_col, clean_col in zip(raw_columns, clean_columns):

        if clean_col == "Label":
            dtype_map[raw_col] = "category"

        elif clean_col == "Group_ID":
            dtype_map[raw_col] = "uint64"

        else:
            dtype_map[raw_col] = np.float32

    df = pd.read_csv(
        path,
        dtype=dtype_map,
        low_memory=False
    )

    df.columns = clean_columns

    return df


def create_stratified_sample(df, max_rows):

    sample_parts = []

    total_rows = len(df)

    for label, group in df.groupby(
        "Label",
        observed=True,
        sort=False
    ):

        class_count = len(group)

        # Keep all very rare classes
        if class_count <= 1000:
            sample_count = class_count

        else:
            sample_count = round(
                max_rows * class_count / total_rows
            )

            sample_count = max(1, min(sample_count, class_count))

        if sample_count == class_count:
            sampled_group = group

        else:
            sampled_group = group.sample(
                n=sample_count,
                random_state=RANDOM_STATE
            )

        sample_parts.append(sampled_group)

    sampled_df = pd.concat(
        sample_parts,
        ignore_index=True
    )

    return sampled_df.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(drop=True)


print("\nSENTINEL AI - CIC-IDS2017 MODEL TRAINING")
print("=" * 65)

print("\nLoading training dataset...")

train_df = load_training_data(TRAIN_PATH)

print(f"Training records: {len(train_df):,}")
print(f"Total columns: {len(train_df.columns)}")

if "Label" not in train_df.columns:
    raise ValueError("Label column is missing.")

if "Group_ID" not in train_df.columns:
    raise ValueError("Group_ID column is missing.")

feature_columns = [
    col for col in train_df.columns
    if col not in ["Label", "Group_ID"]
]

# Remove features that contain no usable training values
all_missing = [
    col for col in feature_columns
    if train_df[col].isna().all()
]

if all_missing:
    print("\nDropping completely empty features:", all_missing)
    feature_columns = [
        col for col in feature_columns
        if col not in all_missing
    ]

print(f"Features used: {len(feature_columns)}")

print("\nOriginal training class distribution:")
print(train_df["Label"].value_counts())


print("\n" + "=" * 65)
print("TRAINING RANDOM FOREST")
print("=" * 65)

rf_sample = create_stratified_sample(
    train_df,
    RF_SAMPLE_SIZE
)

print(f"\nRF training sample: {len(rf_sample):,} rows")
print("\nRF sample class distribution:")
print(rf_sample["Label"].value_counts())

rf_imputer = SimpleImputer(strategy="median")

X_rf = rf_imputer.fit_transform(
    rf_sample[feature_columns]
)

y_rf = rf_sample["Label"].astype(str)

rf_model = RandomForestClassifier(
    n_estimators=50,
    max_depth=20,
    min_samples_leaf=2,
    max_features="sqrt",
    class_weight="balanced_subsample",
    max_samples=0.8,
    n_jobs=2,
    random_state=RANDOM_STATE,
    verbose=1
)

print("\nFitting Random Forest...")

rf_model.fit(X_rf, y_rf)

print("\nRandom Forest training completed!")

del X_rf, y_rf, rf_sample
gc.collect()



print("\n" + "=" * 65)
print("TRAINING ISOLATION FOREST")
print("=" * 65)

benign_df = train_df.loc[
    train_df["Label"] == "BENIGN",
    feature_columns
]

print(f"\nAvailable BENIGN records: {len(benign_df):,}")

if len(benign_df) > IF_SAMPLE_SIZE:

    benign_sample = benign_df.sample(
        n=IF_SAMPLE_SIZE,
        random_state=RANDOM_STATE
    )

else:
    benign_sample = benign_df.copy()

print(f"IF training sample: {len(benign_sample):,} rows")

if_imputer = SimpleImputer(strategy="median")

X_if = if_imputer.fit_transform(benign_sample)

if_model = IsolationForest(
    n_estimators=150,
    max_samples=256,
    contamination="auto",
    random_state=RANDOM_STATE,
    n_jobs=2
)

print("\nFitting Isolation Forest...")

if_model.fit(X_if)

print("\nIsolation Forest training completed!")

del X_if, benign_df, benign_sample, train_df
gc.collect()



print("\n" + "=" * 65)
print("SAVING MODEL ARTIFACTS")
print("=" * 65)

joblib.dump(
    rf_model,
    MODEL_DIR / "random_forest.pkl",
    compress=3
)

joblib.dump(
    if_model,
    MODEL_DIR / "isolation_forest.pkl",
    compress=3
)

preprocessor_bundle = {
    "rf_imputer": rf_imputer,
    "if_imputer": if_imputer,
    "feature_columns": feature_columns,
    "normal_label": "BENIGN",
    "dataset": "CIC-IDS2017"
}

joblib.dump(
    preprocessor_bundle,
    MODEL_DIR / "preprocessor_bundle.pkl",
    compress=3
)

print("\nAll model artifacts saved successfully!")

print("\nSaved files:")
print(MODEL_DIR / "random_forest.pkl")
print(MODEL_DIR / "isolation_forest.pkl")
print(MODEL_DIR / "preprocessor_bundle.pkl")

print("\nMODEL TRAINING COMPLETED!")