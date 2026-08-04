"""
=========================================
Test File for missing.py
=========================================
"""

from datamop.loader import load_csv
from datamop.missing import (
    detect_missing,
    clean_missing_values
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = load_csv(r"C:\Users\Ajay\Downloads\train.csv")

# ---------------------------------------------------
# Original Dataset
# ---------------------------------------------------

print("=" * 50)
print("ORIGINAL DATASET")
print("=" * 50)

print("Shape :", df.shape)

print("\nMissing Values:")
print(detect_missing(df))

# ---------------------------------------------------
# Clean Dataset
# ---------------------------------------------------

cleaned_df = clean_missing_values(
    df,
    threshold=40,
    numeric_method="mean"
)

# ---------------------------------------------------
# Cleaned Dataset
# ---------------------------------------------------

print("\n" + "=" * 50)
print("CLEANED DATASET")
print("=" * 50)

print("Shape :", cleaned_df.shape)

print("\nMissing Values:")
print(detect_missing(cleaned_df))