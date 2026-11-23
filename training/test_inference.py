import pandas as pd
from src.inference import predict_traffic

print("\nSENTINEL AI - INFERENCE TEST")
print("=" * 55)

# Read 5 actual CIC-IDS2017 test records
df = pd.read_csv(
    "data/processed/test.csv",
    nrows=5
)

print("\nInput records:", len(df))

# Generate predictions using real trained models
results = predict_traffic(df)

print("\nPREDICTION RESULTS")
print("=" * 55)

print(results.to_string(index=False))

print("\nINFERENCE TEST PASSED!")