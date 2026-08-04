"""
=========================================
Test File for loader.py
=========================================
"""

from datamop.loader import (
    load_csv,
    dataset_shape,
    dataset_info,
    column_names,
    data_types,
    summary_statistics
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = load_csv(r"C:\Users\Ajay\Downloads\train.csv")

# ---------------------------------------------------
# Display Shape
# ---------------------------------------------------

dataset_shape(df)

# ---------------------------------------------------
# Display Column Names
# ---------------------------------------------------

print()
column_names(df)

# ---------------------------------------------------
# Display Data Types
# ---------------------------------------------------

print()
data_types(df)

# ---------------------------------------------------
# Display Dataset Information
# ---------------------------------------------------

print()
dataset_info(df)

# ---------------------------------------------------
# Display Statistics
# ---------------------------------------------------

print()
summary_statistics(df)