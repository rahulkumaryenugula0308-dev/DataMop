"""
=========================================================
summary.py

This module provides functions to summarize a dataset.

Author : Rahul
Project : DataMop
=========================================================
"""

import pandas as pd

# ----------------------------------------------------------
# 1. Dataset Summary
# ----------------------------------------------------------

def dataset_summary(df):
    """
    Return basic dataset information.
    """

    summary = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }

    return summary


# ----------------------------------------------------------
# 2. Numeric Summary
# ----------------------------------------------------------

def numeric_summary(df):
    """
    Return summary statistics for numeric columns.
    """

    return df.describe()


# ----------------------------------------------------------
# 3. Categorical Summary
# ----------------------------------------------------------

def categorical_summary(df):
    """
    Return summary statistics for categorical columns.
    """

    return df.describe(include=["object"])