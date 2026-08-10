"""
datatype.py

Provides functions for detecting and converting
data types in pandas DataFrames.

Author: Shurthy
Project: DataMop
"""

import pandas as pd


def _validate_dataframe(df):
    """Validate that the input is a pandas DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")


def _validate_column(df, column):
    """Validate that a column exists in the DataFrame."""
    if not isinstance(column, str):
        raise TypeError("Column name must be a string.")

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' not found in DataFrame."
        )


def detect_type(df):
    """
    Detect the datatype of every column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pandas.Series
        Datatype of each column.
    """
    _validate_dataframe(df)

    return df.dtypes


def convert_numeric(df, column):
    """
    Convert a column to numeric datatype.

    Invalid values are converted to NaN.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    column : str
        Column to convert.

    Returns
    -------
    pandas.DataFrame
        Copy of DataFrame with converted column.
    """
    _validate_dataframe(df)
    _validate_column(df, column)

    result = df.copy()

    result[column] = pd.to_numeric(
        result[column],
        errors="coerce"
    )

    return result


def convert_datetime(df, column):
    """
    Convert a column to datetime datatype.

    Invalid date values are converted to NaT.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    column : str
        Column to convert.

    Returns
    -------
    pandas.DataFrame
        Copy of DataFrame with converted column.
    """
    _validate_dataframe(df)
    _validate_column(df, column)

    result = df.copy()

    result[column] = pd.to_datetime(
        result[column],
        errors="coerce"
    )

    return result


def convert_boolean(df, column):
    """
    Convert common text representations to Boolean values.

    Supported values include:

    True:
        yes, true, 1, y

    False:
        no, false, 0, n

    Unknown values are converted to pandas.NA.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    column : str
        Column to convert.

    Returns
    -------
    pandas.DataFrame
        Copy of DataFrame with Boolean conversion.
    """
    _validate_dataframe(df)
    _validate_column(df, column)

    mapping = {
        "yes": True,
        "true": True,
        "1": True,
        "y": True,
        "no": False,
        "false": False,
        "0": False,
        "n": False
    }

    result = df.copy()

    normalized = (
        result[column]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    result[column] = normalized.map(mapping).astype("boolean")

    return result


def datatype_summary(df):
    """
    Generate a summary of every DataFrame column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    dict
        Dictionary containing datatype, missing values,
        unique values and row count.
    """
    _validate_dataframe(df)

    summary = {}

    for column in df.columns:
        summary[column] = {
            "datatype": str(df[column].dtype),
            "missing_values": int(
                df[column].isna().sum()
            ),
            "unique_values": int(
                df[column].nunique(dropna=True)
            ),
            "total_values": int(len(df[column]))
        }

    return summary
