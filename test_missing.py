"""
=========================================
Test File for missing.py
=========================================
"""

from datamop.loader import load_csv
from datamop.missing import (
    detect_missing,
    clean_missing_values,
    fill_constant
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
# ---------------------------------------------------
# Test Constant Fill
# ---------------------------------------------------

print("\n" + "=" * 50)
print("CONSTANT FILL TEST")
print("=" * 50)

constant_df = fill_constant(df, value="Missing")

print("Missing Values After Constant Fill:")
print(detect_missing(constant_df))
# ---------------------------------------------------
# Test Improved Missing Value Detection
# ---------------------------------------------------

import pandas as pd

print("\n" + "=" * 50)
print("SPECIAL MISSING VALUE DETECTION TEST")
print("=" * 50)

sample = pd.DataFrame({
    "Name": ["Rahul", "", "Unknown", None],
    "City": ["Hyderabad", "?", "-", "N/A"],
    "Age": [20, None, 25, 30]
})

print(sample)

print("\nDetected Missing Values:")
print(detect_missing(sample))
