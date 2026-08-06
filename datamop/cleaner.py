"""
DataMop - Automatic Data Cleaning Library

Author: Team DataMop
"""

import pandas as pd
import numpy as np


class DataCleaner:
    """
    Main class for loading, cleaning, summarizing,
    and saving datasets.
    """

    def __init__(self):
        self.df = None
        self.logs = []

    # ----------------------------------------------------
    # Load Dataset
    # ----------------------------------------------------
    def load(self, filepath):
        """
        Load CSV or Excel file.
        """

        try:

            if filepath.endswith(".csv"):
                self.df = pd.read_csv(filepath)

            elif filepath.endswith(".xlsx") or filepath.endswith(".xls"):
                self.df = pd.read_excel(filepath)

            else:
                raise ValueError("Unsupported file format.")

            self.logs.append(f"Dataset loaded successfully from {filepath}")

            print("Dataset Loaded Successfully")

        except Exception as e:
            print("Error:", e)

    # ----------------------------------------------------
    # Dataset Summary
    # ----------------------------------------------------
    def summarize(self):
        """
        Display dataset summary.
        """

        if self.df is None:
            print("No dataset loaded.")
            return

        print("\n========== DATASET SUMMARY ==========")

        print("\nShape:")
        print(self.df.shape)

        print("\nColumns:")
        print(self.df.columns.tolist())

        print("\nData Types:")
        print(self.df.dtypes)

        print("\nMissing Values:")
        print(self.df.isnull().sum())

        print("\nDuplicate Rows:")
        print(self.df.duplicated().sum())

        print("\nStatistical Summary:")
        print(self.df.describe(include="all"))

    # ----------------------------------------------------
    # Clean Dataset
    # ----------------------------------------------------
    def clean(self):
        """
        Perform automatic cleaning.
        """

        if self.df is None:
            print("No dataset loaded.")
            return

        # Remove duplicate rows
        duplicate_count = self.df.duplicated().sum()

        if duplicate_count > 0:
            self.df.drop_duplicates(inplace=True)
            self.logs.append(
                f"Removed {duplicate_count} duplicate rows."
            )

        # Fill missing values
        for column in self.df.columns:

            if self.df[column].dtype == "object":

                missing = self.df[column].isnull().sum()

                if missing > 0:
                    mode = self.df[column].mode()

                    if len(mode) > 0:
                        self.df[column].fillna(mode[0], inplace=True)
                        self.logs.append(
                            f"Filled {missing} missing values in '{column}' using mode."
                        )

            else:

                missing = self.df[column].isnull().sum()

                if missing > 0:
                    median = self.df[column].median()
                    self.df[column].fillna(median, inplace=True)
                    self.logs.append(
                        f"Filled {missing} missing values in '{column}' using median."
                    )

        # Remove leading/trailing spaces
        object_columns = self.df.select_dtypes(include=["object"]).columns

        for col in object_columns:
            self.df[col] = self.df[col].astype(str).str.strip()

        self.logs.append("Removed extra spaces from text columns.")

        # Standardize column names
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        self.logs.append("Standardized column names.")

        print("Cleaning Completed Successfully")

    # ----------------------------------------------------
    # Save Dataset
    # ----------------------------------------------------
    def save(self, filepath):
        """
        Save cleaned dataset.
        """

        if self.df is None:
            print("No dataset loaded.")
            return

        try:

            if filepath.endswith(".csv"):
                self.df.to_csv(filepath, index=False)

            elif filepath.endswith(".xlsx"):
                self.df.to_excel(filepath, index=False)

            else:
                raise ValueError("Unsupported output format.")

            self.logs.append(
                f"Dataset saved successfully to {filepath}"
            )

            print("Dataset Saved Successfully")

        except Exception as e:
            print("Error:", e)

    # ----------------------------------------------------
    # Cleaning Log
    # ----------------------------------------------------
    def cleaning_log(self):
        """
        Print all cleaning operations performed.
        """

        print("\n========== CLEANING LOG ==========")

        if len(self.logs) == 0:
            print("No operations performed.")

        else:
            for i, log in enumerate(self.logs, start=1):
                print(f"{i}. {log}")

    # ----------------------------------------------------
    # Return DataFrame
    # ----------------------------------------------------
    def get_dataframe(self):
        """
        Return cleaned dataframe.
        """

        return self.df