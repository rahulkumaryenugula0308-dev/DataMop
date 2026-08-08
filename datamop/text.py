"""
text.py

This module provides text cleaning functions.

Functions:
    trim_spaces()
    lower_case()
    upper_case()
    title_case()
    normalize_categories()
    clean_text()
"""

import pandas as pd


def trim_spaces(df):
    """
    Remove leading and trailing spaces from text columns.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.strip()
        )

    return cleaned_df


def lower_case(df):
    """
    Convert all text columns to lowercase.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.lower()
        )

    return cleaned_df


def upper_case(df):
    """
    Convert all text columns to uppercase.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.upper()
        )

    return cleaned_df


def title_case(df):
    """
    Convert all text columns to title case.
    """

    cleaned_df = df.copy()

    for column in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.title()
        )

    return cleaned_df


def normalize_categories(df):
    """
    Remove extra spaces and convert text to title case.
    """

    cleaned_df = trim_spaces(df)
    cleaned_df = title_case(cleaned_df)

    return cleaned_df


def clean_text(
    df,
    operation="normalize"
):
    """
    Main text-cleaning function.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    operation : str
        Text cleaning operation.

        Options:
            "trim"
            "lower"
            "upper"
            "title"
            "normalize"

    Returns
    -------
    pandas.DataFrame
        Cleaned DataFrame.
    """

    if operation == "trim":
        return trim_spaces(df)

    elif operation == "lower":
        return lower_case(df)

    elif operation == "upper":
        return upper_case(df)

    elif operation == "title":
        return title_case(df)

    elif operation == "normalize":
        return normalize_categories(df)

    else:
        raise ValueError(
            "operation must be "
            "'trim', 'lower', 'upper', 'title', or 'normalize'"
        )