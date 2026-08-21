"""
DataMop - Outlier Detection and Handling

This module detects and handles numerical outliers
using IQR and Z-score methods.
"""

import pandas as pd
import numpy as np


class OutlierHandler:
    """
    Detect and handle outliers in numerical columns.
    """

    def __init__(self, dataframe=None):
        """
        Initialize OutlierHandler.
        """

        self.df = dataframe
        self.logs = []

    # ==================================================
    # Set Data
    # ==================================================

    def set_data(self, dataframe):
        """
        Set the DataFrame for outlier processing.
        """

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe

        return self.df

    # ==================================================
    # Check Data
    # ==================================================

    def _check_data(self):
        """
        Check whether data is available.
        """

        if self.df is None:
            raise ValueError(
                "No dataset available. "
                "Set or load a dataset first."
            )

    # ==================================================
    # Get Numerical Columns
    # ==================================================

    def get_numerical_columns(self):
        """
        Return numerical columns.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=np.number
        ).columns.tolist()

    # ==================================================
    # IQR Detection
    # ==================================================

    def detect_iqr(
        self,
        column,
        multiplier=1.5
    ):
        """
        Detect outliers using the IQR method.

        Parameters
        ----------
        column : str
            Numerical column.

        multiplier : float
            IQR multiplier. Default = 1.5.

        Returns
        -------
        dict
            Outlier information.
        """

        self._check_data()

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        if not pd.api.types.is_numeric_dtype(
            self.df[column]
        ):
            raise TypeError(
                f"Column '{column}' must be numerical."
            )

        series = self.df[column].dropna()

        if series.empty:
            return {
                "column": column,
                "q1": None,
                "q3": None,
                "iqr": None,
                "lower_bound": None,
                "upper_bound": None,
                "outlier_count": 0,
                "outlier_percentage": 0.0,
                "outliers": pd.Series(
                    dtype=float
                )
            }

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (
            multiplier * iqr
        )

        upper_bound = q3 + (
            multiplier * iqr
        )

        outlier_mask = (
            (self.df[column] < lower_bound)
            |
            (self.df[column] > upper_bound)
        )

        outliers = self.df.loc[
            outlier_mask,
            column
        ]

        outlier_count = len(outliers)

        total_values = len(series)

        percentage = (
            outlier_count / total_values * 100
            if total_values > 0
            else 0
        )

        return {
            "column": column,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": outlier_count,
            "outlier_percentage": round(
                percentage,
                2
            ),
            "outliers": outliers
        }

    # ==================================================
    # Z-Score Detection
    # ==================================================

    def detect_zscore(
        self,
        column,
        threshold=3
    ):
        """
        Detect outliers using Z-score.

        Parameters
        ----------
        column : str
            Numerical column.

        threshold : float
            Z-score threshold. Default = 3.
        """

        self._check_data()

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        if not pd.api.types.is_numeric_dtype(
            self.df[column]
        ):
            raise TypeError(
                f"Column '{column}' must be numerical."
            )

        series = self.df[column]

        mean = series.mean()

        std = series.std()

        if pd.isna(std) or std == 0:

            return {
                "column": column,
                "mean": mean,
                "std": std,
                "threshold": threshold,
                "outlier_count": 0,
                "outlier_percentage": 0.0,
                "outliers": pd.Series(
                    dtype=float
                )
            }

        z_scores = (
            (series - mean) / std
        )

        outlier_mask = (
            z_scores.abs() > threshold
        )

        outliers = self.df.loc[
            outlier_mask,
            column
        ]

        outlier_count = len(outliers)

        total_values = series.notna().sum()

        percentage = (
            outlier_count / total_values * 100
            if total_values > 0
            else 0
        )

        return {
            "column": column,
            "mean": mean,
            "std": std,
            "threshold": threshold,
            "outlier_count": outlier_count,
            "outlier_percentage": round(
                percentage,
                2
            ),
            "outliers": outliers
        }

    # ==================================================
    # Analyze All Columns Using IQR
    # ==================================================

    def analyze_iqr(
        self,
        multiplier=1.5
    ):
        """
        Analyze all numerical columns using IQR.
        """

        self._check_data()

        results = []

        for column in self.get_numerical_columns():

            result = self.detect_iqr(
                column,
                multiplier
            )

            results.append({
                "column": column,
                "q1": result["q1"],
                "q3": result["q3"],
                "iqr": result["iqr"],
                "lower_bound": result[
                    "lower_bound"
                ],
                "upper_bound": result[
                    "upper_bound"
                ],
                "outlier_count": result[
                    "outlier_count"
                ],
                "outlier_percentage": result[
                    "outlier_percentage"
                ]
            })

        return pd.DataFrame(results)

    # ==================================================
    # Analyze All Columns Using Z-Score
    # ==================================================

    def analyze_zscore(
        self,
        threshold=3
    ):
        """
        Analyze all numerical columns using Z-score.
        """

        self._check_data()

        results = []

        for column in self.get_numerical_columns():

            result = self.detect_zscore(
                column,
                threshold
            )

            results.append({
                "column": column,
                "mean": result["mean"],
                "std": result["std"],
                "threshold": result[
                    "threshold"
                ],
                "outlier_count": result[
                    "outlier_count"
                ],
                "outlier_percentage": result[
                    "outlier_percentage"
                ]
            })

        return pd.DataFrame(results)

    # ==================================================
    # Remove IQR Outliers
    # ==================================================

    def remove_iqr_outliers(
        self,
        columns=None,
        multiplier=1.5
    ):
        """
        Remove rows containing IQR outliers.

        Parameters
        ----------
        columns : list, optional
            Columns to process.

        multiplier : float
            IQR multiplier.
        """

        self._check_data()

        if columns is None:
            columns = self.get_numerical_columns()

        before = len(self.df)

        mask = pd.Series(
            True,
            index=self.df.index
        )

        for column in columns:

            result = self.detect_iqr(
                column,
                multiplier
            )

            lower = result["lower_bound"]

            upper = result["upper_bound"]

            if lower is None or upper is None:
                continue

            column_mask = (
                self.df[column].isna()
                |
                (
                    (self.df[column] >= lower)
                    &
                    (self.df[column] <= upper)
                )
            )

            mask &= column_mask

        self.df = self.df.loc[
            mask
        ].reset_index(drop=True)

        removed = before - len(self.df)

        self.logs.append(
            f"Removed {removed} rows using "
            f"IQR outlier detection."
        )

        return self.df

    # ==================================================
    # Remove Z-Score Outliers
    # ==================================================

    def remove_zscore_outliers(
        self,
        columns=None,
        threshold=3
    ):
        """
        Remove rows containing Z-score outliers.
        """

        self._check_data()

        if columns is None:
            columns = self.get_numerical_columns()

        before = len(self.df)

        mask = pd.Series(
            True,
            index=self.df.index
        )

        for column in columns:

            result = self.detect_zscore(
                column,
                threshold
            )

            series = self.df[column]

            mean = result["mean"]

            std = result["std"]

            if pd.isna(std) or std == 0:
                continue

            z_scores = (
                (series - mean) / std
            )

            column_mask = (
                series.isna()
                |
                (z_scores.abs() <= threshold)
            )

            mask &= column_mask

        self.df = self.df.loc[
            mask
        ].reset_index(drop=True)

        removed = before - len(self.df)

        self.logs.append(
            f"Removed {removed} rows using "
            f"Z-score outlier detection."
        )

        return self.df

    # ==================================================
    # Display IQR Report
    # ==================================================

    def display_iqr_report(
        self,
        multiplier=1.5
    ):
        """
        Display IQR outlier report.
        """

        report = self.analyze_iqr(
            multiplier
        )

        print("\n")
        print("=" * 90)
        print("                 DATAMOP IQR OUTLIER REPORT")
        print("=" * 90)

        if report.empty:

            print("No numerical columns found.")

        else:

            print(
                report.to_string(
                    index=False
                )
            )

        print("=" * 90)

    # ==================================================
    # Display Z-Score Report
    # ==================================================

    def display_zscore_report(
        self,
        threshold=3
    ):
        """
        Display Z-score outlier report.
        """

        report = self.analyze_zscore(
            threshold
        )

        print("\n")
        print("=" * 90)
        print("              DATAMOP Z-SCORE OUTLIER REPORT")
        print("=" * 90)

        if report.empty:

            print("No numerical columns found.")

        else:

            print(
                report.to_string(
                    index=False
                )
            )

        print("=" * 90)

    # ==================================================
    # Cleaning Log
    # ==================================================

    def get_log(self):
        """
        Return cleaning log.
        """

        return self.logs

    def display_log(self):
        """
        Display cleaning operations.
        """

        print("\n")
        print("=" * 70)
        print("                 OUTLIER CLEANING LOG")
        print("=" * 70)

        if not self.logs:

            print("No operations performed.")

        else:

            for number, log in enumerate(
                self.logs,
                start=1
            ):

                print(
                    f"{number}. {log}"
                )

        print("=" * 70)