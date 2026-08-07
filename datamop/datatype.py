"""
datatype.py

Functions for detecting and converting data types in pandas DataFrames.
"""

import pandas as pd


def detect_type(df):
    """
    Detect the datatype of each column.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.Series
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    return df.dtypes


def convert_numeric(df, column):
    """
    Convert a column to numeric datatype.

    Parameters
    ----------
    df : pandas.DataFrame
    column : str

    Returns
    -------
    pandas.DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found.")

    result = df.copy()

    result[column] = pd.to_numeric(
        result[column],
        errors="coerce"
    )

    return result


def convert_datetime(df, column):
    """
    Convert a column into datetime datatype.

    Parameters
    ----------
    df : pandas.DataFrame
    column : str

    Returns
    -------
    pandas.DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found.")

    result = df.copy()

    result[column] = pd.to_datetime(
        result[column],
        errors="coerce"
    )

    return result


def convert_boolean(df, column):
    """
    Convert Yes/No/True/False values into Boolean.

    Parameters
    ----------
    df : pandas.DataFrame
    column : str

    Returns
    -------
    pandas.DataFrame
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found.")

    mapping = {
        "yes": True,
        "true": True,
        "1": True,
        "no": False,
        "false": False,
        "0": False
    }

    result = df.copy()

    result[column] = (
        result[column]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )

    return result


def datatype_summary(df):
    """
    Return datatype summary.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    summary = {}

    for column in df.columns:
        summary[column] = {
            "datatype": str(df[column].dtype),
            "missing_values": int(df[column].isna().sum()),
            "unique_values": int(df[column].nunique())
        }

    return summary