"""
duplicates.py

Provides functions for detecting, removing, and analysing
duplicate and near-duplicate records.

Author: Shurthy
Project: DataMop
"""

from difflib import SequenceMatcher

import pandas as pd


def _validate_dataframe(df):
    """Validate that the input is a pandas DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")


def find_duplicates(df, subset=None, keep=False):
    """
    Find duplicate rows in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    subset : list, optional
        Columns to use when identifying duplicates.

    keep : bool or str, default=False
        False returns all duplicate occurrences.
        "first" keeps the first occurrence.
        "last" keeps the last occurrence.

    Returns
    -------
    pandas.DataFrame
        Rows identified as duplicates.

    Raises
    ------
    TypeError
        If df is not a DataFrame.

    ValueError
        If a requested column does not exist.
    """
    _validate_dataframe(df)

    if subset is not None:
        if isinstance(subset, str):
            subset = [subset]

        missing = [column for column in subset if column not in df.columns]

        if missing:
            raise ValueError(
                f"Columns not found in DataFrame: {missing}"
            )

    return df[df.duplicated(subset=subset, keep=keep)].copy()


def drop_duplicates(df, subset=None, keep="first"):
    """
    Remove duplicate rows from a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    subset : list, optional
        Columns used to identify duplicates.

    keep : {"first", "last", False}, default="first"
        Determines which duplicate record to retain.

    Returns
    -------
    pandas.DataFrame
        DataFrame with duplicates removed.
    """
    _validate_dataframe(df)

    if subset is not None:
        if isinstance(subset, str):
            subset = [subset]

        missing = [column for column in subset if column not in df.columns]

        if missing:
            raise ValueError(
                f"Columns not found in DataFrame: {missing}"
            )

    cleaned_df = df.drop_duplicates(
        subset=subset,
        keep=keep
    )

    return cleaned_df.reset_index(drop=True)


def find_near_duplicates(df, threshold=0.90, columns=None):
    """
    Find pairs of rows that are similar to each other.

    Text from selected columns is combined and compared using
    SequenceMatcher.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    threshold : float, default=0.90
        Similarity threshold between 0 and 1.

    columns : list, optional
        Columns to use for comparison.
        If None, all columns are used.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing:
        - row1
        - row2
        - similarity

    Raises
    ------
    TypeError
        If df is not a DataFrame.

    ValueError
        If threshold is outside 0 to 1 or columns are invalid.
    """
    _validate_dataframe(df)

    if not isinstance(threshold, (int, float)):
        raise TypeError("Threshold must be a number.")

    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1.")

    if columns is None:
        columns = list(df.columns)
    elif isinstance(columns, str):
        columns = [columns]

    missing = [column for column in columns if column not in df.columns]

    if missing:
        raise ValueError(
            f"Columns not found in DataFrame: {missing}"
        )

    if len(df) < 2:
        return pd.DataFrame(
            columns=["row1", "row2", "similarity"]
        )

    comparison_df = df[columns].copy()

    # Convert values into normalized strings.
    for column in columns:
        comparison_df[column] = (
            comparison_df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

    row_strings = comparison_df.astype(str).agg(
        " ".join,
        axis=1
    )

    results = []

    # Compare each unique pair only once.
    for i in range(len(row_strings)):
        for j in range(i + 1, len(row_strings)):

            similarity = SequenceMatcher(
                None,
                row_strings.iloc[i],
                row_strings.iloc[j]
            ).ratio()

            if similarity >= threshold:
                results.append({
                    "row1": i,
                    "row2": j,
                    "similarity": round(similarity, 4)
                })

    return pd.DataFrame(
        results,
        columns=["row1", "row2", "similarity"]
    )


def duplicate_summary(df):
    """
    Generate duplicate statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    dict
        Summary containing total rows, duplicate rows,
        unique rows and duplicate percentage.
    """
    _validate_dataframe(df)

    total_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    unique_rows = total_rows - duplicate_rows

    percentage = (
        duplicate_rows / total_rows * 100
        if total_rows > 0
        else 0
    )

    return {
        "total_rows": total_rows,
        "duplicate_rows": duplicate_rows,
        "unique_rows": unique_rows,
        "duplicate_percentage": round(percentage, 2)
    }