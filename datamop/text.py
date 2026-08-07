"""
=========================================================
text.py

This module provides text cleaning functions.

Functions:
1. trim_spaces()
2. lower_case()
3. upper_case()
4. title_case()
5. normalize_categories()

Author : Rahul
Project : DataMop
=========================================================
"""

import pandas as pd


# ----------------------------------------------------------
# 1. Remove Extra Spaces
# ----------------------------------------------------------

def trim_spaces(df):
    """
    Remove leading and trailing spaces from all text columns.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = cleaned_df[column].astype(str).str.strip()

    return cleaned_df


# ----------------------------------------------------------
# 2. Convert Text to Lower Case
# ----------------------------------------------------------

def lower_case(df):
    """
    Convert all text columns to lowercase.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = cleaned_df[column].astype(str).str.lower()

    return cleaned_df


# ----------------------------------------------------------
# 3. Convert Text to Upper Case
# ----------------------------------------------------------

def upper_case(df):
    """
    Convert all text columns to uppercase.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = cleaned_df[column].astype(str).str.upper()

    return cleaned_df


# ----------------------------------------------------------
# 4. Convert Text to Title Case
# ----------------------------------------------------------

def title_case(df):
    """
    Convert all text columns to title case.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = cleaned_df[column].astype(str).str.title()

    return cleaned_df


# ----------------------------------------------------------
# 5. Normalize Categories
# ----------------------------------------------------------

def normalize_categories(df):
    """
    Normalize text by trimming spaces and converting to title case.
    """

    cleaned_df = trim_spaces(df)
    cleaned_df = title_case(cleaned_df)

    return cleaned_df