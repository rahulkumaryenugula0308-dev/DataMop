"""
=========================================================
loader.py
=========================================================

DataMop Data Loading Module

This module loads different types of data files and
automatically detects the file type.

Supported inputs:
    1. CSV
    2. Excel (.xlsx / .xls)
    3. JSON
    4. Pandas DataFrame
"""

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import os
import json
import pandas as pd


# =========================================================
# 1. LOAD CSV FILE
# =========================================================

def load_csv(file_path):
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters
    ----------
    file_path : str
        Path of the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    return pd.read_csv(file_path)


# =========================================================
# 2. LOAD EXCEL FILE
# =========================================================

def load_excel(file_path):
    """
    Load an Excel file into a Pandas DataFrame.

    Supports:
        .xlsx
        .xls

    Parameters
    ----------
    file_path : str
        Path of the Excel file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    return pd.read_excel(file_path)


# =========================================================
# 3. LOAD JSON FILE
# =========================================================

def load_json(file_path):
    """
    Load a JSON file into a Pandas DataFrame.

    The JSON file is first read using Python's json
    module and then converted into a DataFrame.
    """

    # Open JSON file
    with open(file_path, "r", encoding="utf-8") as file:

        data = json.load(file)

    # -----------------------------------------------------
    # JSON contains a list of records
    # -----------------------------------------------------

    if isinstance(data, list):

        return pd.DataFrame(data)

    # -----------------------------------------------------
    # JSON contains a dictionary
    # -----------------------------------------------------

    elif isinstance(data, dict):

        try:

            return pd.DataFrame(data)

        except ValueError:

            return pd.json_normalize(data)

    # -----------------------------------------------------
    # Unsupported JSON structure
    # -----------------------------------------------------

    else:

        raise ValueError(
            "JSON structure cannot be converted to DataFrame."
        )


# =========================================================
# 4. AUTOMATIC FILE LOADER
# =========================================================

def load_file(source):
    """
    Automatically detect the input type and load it.

    Supported:
        CSV
        Excel
        JSON
        Pandas DataFrame

    Parameters
    ----------
    source : str or pandas.DataFrame
        File path or existing DataFrame.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    # -----------------------------------------------------
    # CASE 1: Input is already a DataFrame
    # -----------------------------------------------------

    if isinstance(source, pd.DataFrame):

        print("Detected input type: Pandas DataFrame")

        return source

    # -----------------------------------------------------
    # CASE 2: Check whether file exists
    # -----------------------------------------------------

    if not os.path.exists(source):

        raise FileNotFoundError(
            f"File not found: {source}"
        )

    # -----------------------------------------------------
    # Get file extension
    # -----------------------------------------------------

    extension = os.path.splitext(source)[1].lower()

    # -----------------------------------------------------
    # CASE 3: CSV
    # -----------------------------------------------------

    if extension == ".csv":

        print("Detected file type: CSV")

        return load_csv(source)

    # -----------------------------------------------------
    # CASE 4: Excel
    # -----------------------------------------------------

    elif extension in [".xlsx", ".xls"]:

        print("Detected file type: Excel")

        return load_excel(source)

    # -----------------------------------------------------
    # CASE 5: JSON
    # -----------------------------------------------------

    elif extension == ".json":

        print("Detected file type: JSON")

        return load_json(source)

    # -----------------------------------------------------
    # CASE 6: Unsupported file
    # -----------------------------------------------------

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )