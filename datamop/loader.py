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

Author : Rahul
Project: DataMop
=========================================================
"""


import os
import pandas as pd


class DataLoader:

    def __init__(self):
        self.data = None
        self.filepath = None

    def load(self, filepath):
        """
        Load CSV or Excel file.
        """

        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"File not found: {filepath}"
            )

        # Get file extension
        file_extension = os.path.splitext(filepath)[1].lower()

        # Load CSV
        if file_extension == ".csv":
            self.data = pd.read_csv(filepath)

        # Load Excel
        elif file_extension in [".xlsx", ".xls"]:
            self.data = pd.read_excel(filepath)

        else:
            raise ValueError(
                "Unsupported file format. "
                "Use CSV or Excel files."
            )

        self.filepath = filepath

        print("File loaded successfully!")
        print(f"File: {filepath}")
        print(f"Rows: {self.data.shape[0]}")
        print(f"Columns: {self.data.shape[1]}")

        return self.data

    def get_data(self):
        """
        Return the loaded DataFrame.
        """

        if self.data is None:
            raise ValueError("No file has been loaded.")

        return self.data