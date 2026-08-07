"""
duplicates.py

Functions for finding and removing duplicate records.
"""

import pandas as pd
from difflib import SequenceMatcher


def find_duplicates(df):
    """
    Return duplicate rows.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    return df[df.duplicated()]


def drop_duplicates(df):
    """
    Remove duplicate rows.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    return df.drop_duplicates()


def find_near_duplicates(df, threshold=0.90):
    """
    Find near duplicate rows using similarity matching.

    Parameters
    ----------
    df : pandas.DataFrame
    threshold : float

    Returns
    -------
    list
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    rows = df.astype(str).agg(" ".join, axis=1)

    similar = []

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):

            score = SequenceMatcher(
                None,
                rows.iloc[i],
                rows.iloc[j]
            ).ratio()

            if score >= threshold:
                similar.append({
                    "Row1": i,
                    "Row2": j,
                    "Similarity": round(score, 2)
                })

    return similar


def duplicate_summary(df):
    """
    Return duplicate statistics.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    duplicates = int(df.duplicated().sum())

    summary = {
        "Total Rows": len(df),
        "Duplicate Rows": duplicates,
        "Unique Rows": len(df) - duplicates,
        "Duplicate Percentage": round(
            (duplicates / len(df)) * 100,
            2
        ) if len(df) > 0 else 0
    }

    return summary