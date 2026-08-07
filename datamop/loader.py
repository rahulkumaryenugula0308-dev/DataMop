"""
=========================================================
loader.py
=========================================================

Purpose:
--------
This module is responsible for loading datasets into
the DataMop project.

Supported file types:
1. CSV
2. Excel (.xlsx)
3. JSON

Author : Rahul
Project: DataMop
=========================================================
"""

# -------------------------------------------------------
# Import Required Library
# -------------------------------------------------------

import os
import pandas as pd


# =======================================================
# 1. Load CSV File
# =======================================================

def load_csv(file_path):
    """
    Load a CSV file.

    Parameters
    ----------
    file_path : str
        Path of the CSV file.

    Returns
    -------
    pandas.DataFrame
    """

    # Check whether the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read CSV file
    df = pd.read_csv(file_path)

    return df


# =======================================================
# 2. Load Excel File
# =======================================================

def load_excel(file_path):
    """
    Load an Excel (.xlsx) file.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)

    return df


# =======================================================
# 3. Load JSON File
# =======================================================

def load_json(file_path):
    """
    Load a JSON file.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_json(file_path)

    return df


# =======================================================
# 4. Display Dataset Information
# =======================================================

def dataset_info(df):
    """
    Display dataset information.
    """

    print("=" * 50)
    print("DATASET INFORMATION")
    print("=" * 50)

    print(df.info())


# =======================================================
# 5. Display Dataset Shape
# =======================================================

def dataset_shape(df):
    """
    Print number of rows and columns.
    """

    rows, columns = df.shape

    print("=" * 50)
    print("DATASET SHAPE")
    print("=" * 50)

    print("Rows    :", rows)
    print("Columns :", columns)


# =======================================================
# 6. Display Column Names
# =======================================================

def column_names(df):
    """
    Print all column names.
    """

    print("=" * 50)
    print("COLUMN NAMES")
    print("=" * 50)

    for column in df.columns:
        print(column)


# =======================================================
# 7. Display Data Types
# =======================================================

def data_types(df):
    """
    Print datatype of every column.
    """

    print("=" * 50)
    print("DATA TYPES")
    print("=" * 50)

    print(df.dtypes)


# =======================================================
# 8. Display Basic Statistics
# =======================================================

def summary_statistics(df):
    """
    Display statistical summary.
    """

    print("=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)

    print(df.describe(include="all"))
# ----------------------------------------------------------
# 9.Load Existing DataFrame
# ----------------------------------------------------------

def load_dataframe(df):
    """
    Return a copy of an existing Pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pandas.DataFrame
        Copy of the DataFrame.
    """

    return df.copy()