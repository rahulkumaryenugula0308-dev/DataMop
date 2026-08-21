"""
DataMop - Smart Correlation Analysis

This module performs intelligent correlation analysis
using the DataMop ColumnProfiler.
"""

import os

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from datamop.profiler import ColumnProfiler


class CorrelationAnalyzer:
    """
    Intelligent correlation analyzer.
    """

    def __init__(
        self,
        dataframe=None,
        output_dir="visualizations"
    ):
        self.df = dataframe

        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

        self.profiler = ColumnProfiler(
            dataframe
        )

        self.correlation_matrix = None

    # ==================================================
    # Set Data
    # ==================================================

    def set_data(self, dataframe):
        """
        Set the DataFrame.
        """

        if not isinstance(
            dataframe,
            pd.DataFrame
        ):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe

        self.profiler.set_data(
            dataframe
        )

        return self.df

    # ==================================================
    # Check Data
    # ==================================================

    def _check_data(self):

        if self.df is None:
            raise ValueError(
                "No dataset available."
            )

        if self.df.empty:
            raise ValueError(
                "Dataset is empty."
            )

    # ==================================================
    # Get Correlation Columns
    # ==================================================

    def get_correlation_columns(self):
        """
        Return appropriate numerical columns
        for correlation analysis.

        ID columns are excluded.
        """

        self._check_data()

        groups = {}

        profile = (
            self.profiler.profile()
        )

        continuous = profile.loc[
            profile["column_type"]
            == "numeric_continuous",
            "column"
        ].tolist()

        discrete = profile.loc[
            profile["column_type"]
            == "numeric_discrete",
            "column"
        ].tolist()

        # Include continuous variables.
        # Include discrete variables only when
        # there are enough meaningful numeric columns.

        columns = continuous + discrete

        # Remove ID columns explicitly.
        id_columns = profile.loc[
            profile["column_type"] == "id",
            "column"
        ].tolist()

        columns = [
            column
            for column in columns
            if column not in id_columns
        ]

        return columns

    # ==================================================
    # Calculate Correlation
    # ==================================================

    def calculate(self):
        """
        Calculate Pearson correlation matrix.
        """

        self._check_data()

        columns = (
            self.get_correlation_columns()
        )

        if len(columns) < 2:

            self.correlation_matrix = (
                pd.DataFrame()
            )

            return self.correlation_matrix

        self.correlation_matrix = (
            self.df[columns]
            .corr()
        )

        return self.correlation_matrix

    # ==================================================
    # Find Strong Correlations
    # ==================================================

    def find_strong_correlations(
        self,
        threshold=0.70
    ):
        """
        Find strongly correlated variable pairs.

        Parameters
        ----------
        threshold : float
            Absolute correlation threshold.
        """

        matrix = self.calculate()

        if matrix.empty:

            return pd.DataFrame(
                columns=[
                    "column_1",
                    "column_2",
                    "correlation",
                    "strength"
                ]
            )

        results = []

        columns = matrix.columns

        for i in range(
            len(columns)
        ):

            for j in range(
                i + 1,
                len(columns)
            ):

                correlation = matrix.iloc[
                    i,
                    j
                ]

                if pd.isna(correlation):
                    continue

                if abs(correlation) >= threshold:

                    absolute_value = abs(
                        correlation
                    )

                    if absolute_value >= 0.90:

                        strength = "Very Strong"

                    elif absolute_value >= 0.70:

                        strength = "Strong"

                    else:

                        strength = "Moderate"

                    results.append({
                        "column_1":
                            columns[i],

                        "column_2":
                            columns[j],

                        "correlation":
                            round(
                                correlation,
                                4
                            ),

                        "strength":
                            strength
                    })

        return pd.DataFrame(
            results
        )

    # ==================================================
    # Generate Heatmap
    # ==================================================

    def heatmap(
        self,
        filename="smart_correlation_heatmap.png"
    ):
        """
        Generate correlation heatmap.
        """

        matrix = self.calculate()

        if matrix.empty:

            print(
                "Not enough suitable numerical "
                "columns for correlation analysis."
            )

            return None

        plt.figure(
            figsize=(12, 8)
        )

        sns.heatmap(
            matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=False
        )

        plt.title(
            "DataMop Smart Correlation Heatmap"
        )

        plt.tight_layout()

        filepath = os.path.join(
            self.output_dir,
            filename
        )

        plt.savefig(
            filepath,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

        return filepath

    # ==================================================
    # Display Correlation Report
    # ==================================================

    def display_report(self):
        """
        Display correlation analysis report.
        """

        self._check_data()

        columns = (
            self.get_correlation_columns()
        )

        print("\n")
        print("=" * 80)
        print("             DATAMOP CORRELATION ANALYSIS")
        print("=" * 80)

        print("\nColumns used:")
        print(
            ", ".join(columns)
            if columns
            else "None"
        )

        matrix = self.calculate()

        print("\nCorrelation Matrix:")
        print("-" * 80)

        if matrix.empty:

            print(
                "Not enough numerical columns."
            )

        else:

            print(
                matrix.to_string()
            )

        print("\nStrong Correlations:")
        print("-" * 80)

        strong = (
            self.find_strong_correlations()
        )

        if strong.empty:

            print(
                "No strong correlations found."
            )

        else:

            print(
                strong.to_string(
                    index=False
                )
            )

        print("=" * 80)