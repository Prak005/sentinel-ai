from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from src.preprocessing import clean_dataframe, prepare_data


# Generate synthetic network traffic records
records = []

for i in range(20):
    records.append({
        "Flow Duration": 1000 + (i * 100),
        "Total Fwd Packets": 5 + i,
        "Protocol": ["TCP", "UDP"][i % 2],
        "Destination Port": [80, 443, 53][i % 3],
        "Label": "BENIGN" if i < 10 else "DDoS"
    })

df = pd.DataFrame(records)

print("Original dataset shape:", df.shape)



# Introduce some data quality issues for testing

# Convert integer columns to float first
df["Flow Duration"] = df["Flow Duration"].astype(float)
df["Total Fwd Packets"] = df["Total Fwd Packets"].astype(float)

# Introduce missing and infinite values
df.loc[2, "Flow Duration"] = np.nan
df.loc[5, "Total Fwd Packets"] = np.inf
df.loc[4, "Protocol"] = None


# Add a duplicate record
df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

# Add a record without a target label
df.loc[len(df)] = [9000, 9, "TCP", 80, None]


print("\nTesting data cleaning...")

cleaned_df = clean_dataframe(df)

print("Rows before cleaning:", len(df))
print("Rows after cleaning:", len(cleaned_df))
print("Remaining missing values:", cleaned_df.isnull().sum().sum())


print("\nTesting preprocessing pipeline...")

X_train, X_test, y_train, y_test, preprocessor = prepare_data(df)
# Save preprocessing pipeline and feature information

cleaned_df = clean_dataframe(df)

feature_columns = cleaned_df.drop(
    columns=["Label"]
).columns.tolist()

Path("models").mkdir(parents=True, exist_ok=True)

joblib.dump(
    {
        "preprocessor": preprocessor,
        "feature_columns": feature_columns
    },
    "models/preprocessor_bundle.pkl"
)

print("Preprocessor saved successfully!")

print("\nFinal Results")
print("---------------------------")
print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)
print("Training labels:", y_train.value_counts().to_dict())
print("Testing labels:", y_test.value_counts().to_dict())

print("\nPreprocessing pipeline tested successfully!")

from src.random_forest import train_random_forest

print("\nStarting Random Forest testing...")

model, predictions = train_random_forest(
    X_train,
    y_train,
    X_test,
    y_test
)


from src.anomaly_detection import train_isolation_forest

print("\nStarting Isolation Forest testing...")

anomaly_model, anomaly_predictions, anomaly_scores = (
    train_isolation_forest(
        X_train,
        y_train,
        X_test,
        y_test
    )
)


from src.hybrid_detection import detect_intrusions

print("\nStarting Hybrid Detection Engine...")

hybrid_results = detect_intrusions(
    X_test,
    model,
    anomaly_model
)

print("\nHybrid Detection Results")
print("-------------------------------")

print(hybrid_results.to_string(index=False))

print("\nFinal Status Summary:")
print(
    hybrid_results["Final Status"].value_counts()
)

from src.inference import predict_traffic

print("\nTesting Sentinel AI Inference Engine...")

# Use raw traffic records, not preprocessed X_test
sample_input = df.drop(columns=["Label"]).head(5)

results = predict_traffic(sample_input)

print("\nSentinel AI Detection Results")
print("--------------------------------")

print(results.to_string(index=False))

print("\nDetection Summary:")
print(results["Final Status"].value_counts())