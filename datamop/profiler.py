"""
DataMop - Column Profiler

Automatically determines the characteristics of
dataset columns for intelligent analysis and visualization.
"""

import pandas as pd
import numpy as np


class ColumnProfiler:

    def __init__(self, dataframe=None):

        self.df = dataframe

    # ==================================================
    # Set Data
    # ==================================================

    def set_data(self, dataframe):

        if not isinstance(
            dataframe,
            pd.DataFrame
        ):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe

        return self.df

    # ==================================================
    # Check Data
    # ==================================================

    def _check_data(self):

        if self.df is None:
            raise ValueError(
                "No dataset available."
            )

    # ==================================================
    # Profile Column
    # ==================================================

    def profile_column(self, column):

        self._check_data()

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        series = self.df[column]

        dtype = series.dtype

        total = len(series)

        missing = int(
            series.isna().sum()
        )

        unique = int(
            series.nunique(
                dropna=True
            )
        )

        if total > 0:

            cardinality_ratio = (
                unique / total
            )

        else:

            cardinality_ratio = 0

        # ----------------------------------------------
        # ID detection
        # ----------------------------------------------

        normalized_name = (
            column.lower()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
        )

        id_keywords = [
            "id",
            "code",
            "key",
            "uuid",
            "identifier"
        ]

        looks_like_id = any(
            keyword in normalized_name
            for keyword in id_keywords
        )

        if (
            looks_like_id
            and cardinality_ratio > 0.8
        ):

            column_type = "id"

        # ----------------------------------------------
        # Datetime
        # ----------------------------------------------

        elif pd.api.types.is_datetime64_any_dtype(
            dtype
        ):

            column_type = "datetime"

        # ----------------------------------------------
        # Boolean
        # ----------------------------------------------

        elif pd.api.types.is_bool_dtype(
            dtype
        ):

            column_type = "binary"

        # ----------------------------------------------
        # Numeric
        # ----------------------------------------------

        elif pd.api.types.is_numeric_dtype(
            dtype
        ):

            if unique <= 10:

                column_type = "numeric_discrete"

            else:

                column_type = "numeric_continuous"

        # ----------------------------------------------
        # Categorical
        # ----------------------------------------------

        else:

            if unique == 2:

                column_type = "binary"

            elif cardinality_ratio > 0.5:

                column_type = "high_cardinality"

            else:

                column_type = "categorical"

        return {
            "column": column,
            "dtype": str(dtype),
            "column_type": column_type,
            "rows": total,
            "missing": missing,
            "unique": unique,
            "cardinality_ratio":
                round(
                    cardinality_ratio,
                    4
                )
        }

    # ==================================================
    # Profile Entire Dataset
    # ==================================================

    def profile(self):

        self._check_data()

        results = []

        for column in self.df.columns:

            results.append(
                self.profile_column(
                    column
                )
            )

        return pd.DataFrame(
            results
        )

    # ==================================================
    # Get Columns By Type
    # ==================================================

    def get_columns_by_type(
        self,
        column_type
    ):

        report = self.profile()

        return report.loc[
            report["column_type"]
            == column_type,
            "column"
        ].tolist()

    # ==================================================
    # Display Profile
    # ==================================================

    def display_profile(self):

        report = self.profile()

        print("\n")
        print("=" * 90)
        print("                 DATAMOP COLUMN PROFILE")
        print("=" * 90)

        print(
            report.to_string(
                index=False
            )
        )

        print("=" * 90)