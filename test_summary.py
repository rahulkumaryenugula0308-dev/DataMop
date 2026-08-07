from datamop.loader import load_csv
from datamop.summary import (
    dataset_summary,
    numeric_summary,
    categorical_summary
)

# Load dataset
df = load_csv(r"C:\Users\Ajay\Downloads\train.csv")

print("=" * 50)
print("DATASET SUMMARY")
print("=" * 50)

print(dataset_summary(df))

print("\n" + "=" * 50)
print("NUMERIC SUMMARY")
print("=" * 50)

print(numeric_summary(df))

print("\n" + "=" * 50)
print("CATEGORICAL SUMMARY")
print("=" * 50)

print(categorical_summary(df))