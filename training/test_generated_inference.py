import pandas as pd
from src.inference import predict_traffic

file_path = (
    "data/raw/GeneratedLabelledFlows/"
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)

# Read 10 actual records
df = pd.read_csv(
    file_path,
    nrows=10,
    low_memory=False
)

# Normalize column names
df.columns = (
    df.columns.astype(str)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

print("\nGENERATED LABELLED FLOWS INFERENCE TEST")
print("=" * 60)

# Existing trained models
results = predict_traffic(df)

# Preserve metadata alongside predictions
metadata_columns = [
    "Timestamp",
    "Source IP",
    "Destination IP",
    "Label"
]

metadata = df[
    [col for col in metadata_columns if col in df.columns]
].reset_index(drop=True)

final_output = pd.concat(
    [metadata, results.reset_index(drop=True)],
    axis=1
)

print(final_output.to_string(index=False))

print("\nINFERENCE TEST PASSED!")