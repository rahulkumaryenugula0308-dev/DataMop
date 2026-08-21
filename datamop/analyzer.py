"""
DataMop - Dataset Analyzer

This module analyzes a pandas DataFrame and provides
information about structure, data types, missing values,
duplicates, numerical columns, and categorical columns.
"""

import pandas as pd
import numpy as np


class DataAnalyzer:
    """
    Analyze a dataset and generate a data-quality summary.
    """

    def __init__(self, dataframe=None):
        """
        Initialize the DataAnalyzer.

        Parameters
        ----------
        dataframe : pandas.DataFrame, optional
            Dataset to analyze.
        """

        self.df = dataframe

    # --------------------------------------------------
    # Set Data
    # --------------------------------------------------

    def set_data(self, dataframe):
        """
        Set the DataFrame for analysis.
        """

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        self.df = dataframe

        return self.df

    # --------------------------------------------------
    # Validate Data
    # --------------------------------------------------

    def _check_data(self):
        """
        Check whether a dataset is available.
        """

        if self.df is None:
            raise ValueError(
                "No dataset available. Load a dataset first."
            )

    # --------------------------------------------------
    # Dataset Shape
    # --------------------------------------------------

    def get_shape(self):
        """
        Return number of rows and columns.
        """

        self._check_data()

        rows, columns = self.df.shape

        return {
            "rows": rows,
            "columns": columns
        }

    # --------------------------------------------------
    # Column Information
    # --------------------------------------------------

    def get_column_info(self):
        """
        Return information about every column.
        """

        self._check_data()

        information = []

        for column in self.df.columns:

            information.append({
                "column": column,
                "data_type": str(self.df[column].dtype),
                "non_null": int(self.df[column].notna().sum()),
                "missing": int(self.df[column].isna().sum()),
                "unique": int(self.df[column].nunique())
            })

        return pd.DataFrame(information)

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    def get_missing_values(self):
        """
        Analyze missing values.
        """

        self._check_data()

        missing_count = self.df.isnull().sum()

        missing_percentage = (
            missing_count / len(self.df)
        ) * 100

        result = pd.DataFrame({
            "column": self.df.columns,
            "missing_count": missing_count.values,
            "missing_percentage": missing_percentage.values
        })

        result = result[
            result["missing_count"] > 0
        ]

        return result.sort_values(
            by="missing_percentage",
            ascending=False
        )

    # --------------------------------------------------
    # Duplicate Rows
    # --------------------------------------------------

    def get_duplicates(self):
        """
        Return number of duplicate rows.
        """

        self._check_data()

        duplicate_count = int(
            self.df.duplicated().sum()
        )

        return {
            "duplicate_rows": duplicate_count
        }

    # --------------------------------------------------
    # Numerical Columns
    # --------------------------------------------------

    def get_numerical_columns(self):
        """
        Return numerical column names.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=np.number
        ).columns.tolist()

    # --------------------------------------------------
    # Categorical Columns
    # --------------------------------------------------

    def get_categorical_columns(self):
        """
        Return categorical/text column names.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=["object", "category", "string"]
        ).columns.tolist()

    # --------------------------------------------------
    # Numerical Statistics
    # --------------------------------------------------

    def get_numerical_statistics(self):
        """
        Generate descriptive statistics for numerical columns.
        """

        self._check_data()

        numerical_columns = self.get_numerical_columns()

        if not numerical_columns:
            return pd.DataFrame()

        return self.df[numerical_columns].describe().T

    # --------------------------------------------------
    # Categorical Statistics
    # --------------------------------------------------

    def get_categorical_statistics(self):
        """
        Generate statistics for categorical columns.
        """

        self._check_data()

        categorical_columns = self.get_categorical_columns()

        result = []

        for column in categorical_columns:

            value_counts = self.df[column].value_counts(
                dropna=False
            )

            top_value = (
                value_counts.index[0]
                if len(value_counts) > 0
                else None
            )

            top_frequency = (
                int(value_counts.iloc[0])
                if len(value_counts) > 0
                else 0
            )

            result.append({
                "column": column,
                "unique_values": int(
                    self.df[column].nunique(
                        dropna=False
                    )
                ),
                "top_value": top_value,
                "top_frequency": top_frequency
            })

        return pd.DataFrame(result)

    # --------------------------------------------------
    # Data Quality Score
    # --------------------------------------------------

    def get_quality_score(self):
        """
        Calculate a basic data quality score.

        The score considers missing values and duplicate rows.
        """

        self._check_data()

        total_cells = self.df.shape[0] * self.df.shape[1]

        if total_cells == 0:
            return 0.0

        missing_cells = int(
            self.df.isnull().sum().sum()
        )

        duplicate_rows = int(
            self.df.duplicated().sum()
        )

        missing_ratio = missing_cells / total_cells

        duplicate_ratio = (
            duplicate_rows / len(self.df)
            if len(self.df) > 0
            else 0
        )

        score = 100 - (
            (missing_ratio * 70)
            + (duplicate_ratio * 30)
        )

        score = max(0, min(100, score))

        return round(score, 2)

    # --------------------------------------------------
    # Complete Analysis
    # --------------------------------------------------

    def analyze(self):
        """
        Generate complete dataset analysis.
        """

        self._check_data()

        return {
            "shape": self.get_shape(),
            "columns": self.get_column_info(),
            "missing_values": self.get_missing_values(),
            "duplicates": self.get_duplicates(),
            "numerical_columns": self.get_numerical_columns(),
            "categorical_columns": self.get_categorical_columns(),
            "numerical_statistics": self.get_numerical_statistics(),
            "categorical_statistics": self.get_categorical_statistics(),
            "quality_score": self.get_quality_score()
        }

    # --------------------------------------------------
    # Display Report
    # --------------------------------------------------

    def display_report(self):
        """
        Display a human-readable analysis report.
        """

        self._check_data()

        shape = self.get_shape()
        duplicates = self.get_duplicates()

        print("\n")
        print("=" * 60)
        print("             DATAMOP DATA ANALYSIS")
        print("=" * 60)

        print("\nDATASET OVERVIEW")
        print("-" * 60)

        print(f"Rows              : {shape['rows']}")
        print(f"Columns           : {shape['columns']}")
        print(f"Duplicate Rows    : {duplicates['duplicate_rows']}")

        print("\nCOLUMN INFORMATION")
        print("-" * 60)

        print(self.get_column_info().to_string(index=False))

        print("\nMISSING VALUES")
        print("-" * 60)

        missing = self.get_missing_values()

        if missing.empty:
            print("No missing values found.")
        else:
            print(missing.to_string(index=False))

        print("\nNUMERICAL COLUMNS")
        print("-" * 60)

        numerical = self.get_numerical_columns()

        if numerical:
            print(", ".join(numerical))
        else:
            print("No numerical columns found.")

        print("\nCATEGORICAL COLUMNS")
        print("-" * 60)

        categorical = self.get_categorical_columns()

        if categorical:
            print(", ".join(categorical))
        else:
            print("No categorical columns found.")

        print("\nNUMERICAL STATISTICS")
        print("-" * 60)

        numerical_stats = self.get_numerical_statistics()

        if numerical_stats.empty:
            print("No numerical columns available.")
        else:
            print(numerical_stats.to_string())

        print("\nCATEGORICAL STATISTICS")
        print("-" * 60)

        categorical_stats = self.get_categorical_statistics()

        if categorical_stats.empty:
            print("No categorical columns available.")
        else:
            print(categorical_stats.to_string(index=False))

        print("\nDATA QUALITY SCORE")
        print("-" * 60)

        print(
            f"{self.get_quality_score()} / 100"
        )

        print("\n" + "=" * 60)
        print("             ANALYSIS COMPLETED")
        print("=" * 60)