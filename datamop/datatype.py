"""
datatype.py
===========

Module for detecting and converting data types
in a pandas DataFrame.

Author : Shurthy
Project : DataMop
"""

import pandas as pd


def detect_type(df):
    """
    Display the datatype of every column.

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
    Convert a column into numeric datatype.

    Invalid values become NaN.

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
        raise KeyError(f"Column '{column}' not found.")

    df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def convert_datetime(df, column):
    """
    Convert a column into datetime datatype.

    Invalid values become NaT.

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
        raise KeyError(f"Column '{column}' not found.")

    df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def convert_boolean(df, column):
    """
    Convert Yes/No, True/False, Y/N, 1/0
    into Boolean datatype.

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
        raise KeyError(f"Column '{column}' not found.")

    mapping = {
        "yes": True,
        "no": False,
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "y": True,
        "n": False
    }

    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )

    return df


def datatype_summary(df):
    """
    Display datatype summary.

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
        summary[column] = str(df[column].dtype)

    return summary