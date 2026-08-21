"""
DataMop - Automatic Data Visualization

This module automatically generates visualizations
for numerical, categorical, and missing-value data.
"""

import os

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from datamop.profiler import ColumnProfiler
from datamop.correlation import CorrelationAnalyzer


class DataVisualizer:
    """
    Automatic visualization engine for DataMop.
    """

    def __init__(self, dataframe=None, output_dir="visualizations"):
        """
        Initialize DataVisualizer.

        Parameters
        ----------
        dataframe : pandas.DataFrame, optional
            Dataset to visualize.

        output_dir : str
            Folder where generated charts are stored.
        """

        self.df = dataframe

        self.profiler = ColumnProfiler(
        dataframe
        )
        
        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )
        self.correlation_analyzer = CorrelationAnalyzer(
        dataframe,
        output_dir=output_dir
        )

        self.generated_files = []

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
       
       self.correlation_analyzer.set_data(
       dataframe
       )

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
                "No dataset available."
            )

        if self.df.empty:
            raise ValueError(
                "Dataset is empty."
            )

    # ==================================================
    # Numerical Columns
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
    # Categorical Columns
    # ==================================================

    def get_categorical_columns(self):
        """
        Return categorical columns.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=[
                "object",
                "category",
                "string",
                "bool"
            ]
        ).columns.tolist()
    # ==================================================
    # Smart Column Groups
    # ==================================================

    def get_column_groups(self):
        """
        Get columns grouped according to the
        DataMop ColumnProfiler.
        """

        profile = self.profiler.profile()

        return {
            "id": profile.loc[
                profile["column_type"] == "id",
                "column"
            ].tolist(),

            "binary": profile.loc[
                profile["column_type"] == "binary",
                "column"
            ].tolist(),

            "continuous": profile.loc[
                profile["column_type"]
                == "numeric_continuous",
                "column"
            ].tolist(),

            "discrete": profile.loc[
                profile["column_type"]
                == "numeric_discrete",
                "column"
            ].tolist(),

            "categorical": profile.loc[
                profile["column_type"]
                == "categorical",
                "column"
            ].tolist(),

            "high_cardinality": profile.loc[
                profile["column_type"]
                == "high_cardinality",
                "column"
            ].tolist(),

            "datetime": profile.loc[
                profile["column_type"]
                == "datetime",
                "column"
            ].tolist()
        }
    # ==================================================
    # Save Figure
    # ==================================================

    def _save_figure(self, filename):
        """
        Save current matplotlib figure.
        """

        filepath = os.path.join(
            self.output_dir,
            filename
        )

        plt.tight_layout()

        plt.savefig(
            filepath,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

        self.generated_files.append(
            filepath
        )

        return filepath

    # ==================================================
    # Histogram
    # ==================================================

    def histogram(
        self,
        column,
        bins=30
    ):
        """
        Generate histogram for a numerical column.
        """

        self._check_data()

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        plt.figure(
            figsize=(10, 6)
        )

        sns.histplot(
            data=self.df,
            x=column,
            bins=bins,
            kde=True
        )

        plt.title(
            f"Distribution of {column}"
        )

        plt.xlabel(column)

        plt.ylabel("Frequency")

        filename = (
            f"histogram_{column}.png"
        )

        return self._save_figure(
            filename
        )

    # ==================================================
    # Box Plot
    # ==================================================

    def boxplot(self, column):
        """
        Generate box plot for a numerical column.
        """

        self._check_data()

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        plt.figure(
            figsize=(10, 6)
        )

        sns.boxplot(
            data=self.df,
            y=column
        )

        plt.title(
            f"Box Plot of {column}"
        )

        plt.ylabel(column)

        filename = (
            f"boxplot_{column}.png"
        )

        return self._save_figure(
            filename
        )

    # ==================================================
    # Categorical Bar Chart
    # ==================================================

    def bar_chart(
        self,
        column,
        top_n=15
    ):
        """
        Generate frequency bar chart.
        """

        self._check_data()

        if column not in self.df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        counts = (
            self.df[column]
            .value_counts(
                dropna=False
            )
            .head(top_n)
        )

        plt.figure(
            figsize=(10, 6)
        )

        counts.plot(
            kind="bar"
        )

        plt.title(
            f"Top Categories - {column}"
        )

        plt.xlabel(column)

        plt.ylabel("Frequency")

        plt.xticks(
            rotation=45,
            ha="right"
        )

        filename = (
            f"bar_{column}.png"
        )

        return self._save_figure(
            filename
        )

    # ==================================================
    # Missing Value Chart
    # ==================================================

    def missing_value_chart(self):
        """
        Generate missing-value chart.
        """

        self._check_data()

        missing = (
            self.df.isnull()
            .sum()
            .sort_values(
                ascending=False
            )
        )

        missing = missing[
            missing > 0
        ]

        if missing.empty:

            print(
                "No missing values found."
            )

            return None

        plt.figure(
            figsize=(12, 6)
        )

        missing.plot(
            kind="bar"
        )

        plt.title(
            "Missing Values by Column"
        )

        plt.xlabel("Column")

        plt.ylabel(
            "Number of Missing Values"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        filename = (
            "missing_values.png"
        )

        return self._save_figure(
            filename
        )

    # ==================================================
    # Correlation Heatmap
    # ==================================================

    def correlation_heatmap(self):
        """
        Generate intelligent correlation heatmap.
        """

        self._check_data()

        return self.correlation_analyzer.heatmap(
           filename="correlation_heatmap.png"
       )

    # ==================================================
    # Generate Smart Numerical Visualizations
    # ==================================================

    def generate_numerical_visualizations(
        self
    ):
        """
        Generate visualizations for continuous
        numerical columns only.

        Discrete numerical columns are handled
        using bar charts.
        """

        groups = (
            self.get_column_groups()
        )

        files = []

        # ----------------------------------------------
        # Continuous Numerical Columns
        # ----------------------------------------------

        for column in groups["continuous"]:

            histogram_file = (
                self.histogram(
                    column
                )
            )

            boxplot_file = (
                self.boxplot(
                    column
                )
            )

            files.append(
                histogram_file
            )

            files.append(
                boxplot_file
            )

        return files

        # ==================================================
    # Generate Smart Categorical Visualizations
    # ==================================================

    def generate_categorical_visualizations(
        self,
        top_n=15
    ):
        """
        Generate bar charts for:

        - Binary columns
        - Discrete numerical columns
        - Categorical columns

        High-cardinality and ID columns are skipped.
        """

        groups = (
            self.get_column_groups()
        )

        files = []

        # ----------------------------------------------
        # Binary
        # ----------------------------------------------

        for column in groups["binary"]:

            file = self.bar_chart(
                column,
                top_n=top_n
            )

            files.append(file)

        # ----------------------------------------------
        # Discrete Numerical
        # ----------------------------------------------

        for column in groups["discrete"]:

            file = self.bar_chart(
                column,
                top_n=top_n
            )

            files.append(file)

        # ----------------------------------------------
        # Categorical
        # ----------------------------------------------

        for column in groups["categorical"]:

            unique_count = (
                self.df[column]
                .nunique(
                    dropna=False
                )
            )

            if unique_count <= 50:

                file = self.bar_chart(
                    column,
                    top_n=top_n
                )

                files.append(file)

        return files
    # ==================================================
    # Display Smart Visualization Plan
    # ==================================================

    def display_visualization_plan(self):
        """
        Display the visualization decisions made
        by DataMop.
        """

        groups = (
            self.get_column_groups()
        )

        print("\n")
        print("=" * 80)
        print("              DATAMOP VISUALIZATION PLAN")
        print("=" * 80)

        print("\nCONTINUOUS NUMERICAL")
        print("-" * 80)

        for column in groups["continuous"]:

            print(
                f"{column} → Histogram + Boxplot"
            )

        print("\nDISCRETE NUMERICAL")
        print("-" * 80)

        for column in groups["discrete"]:

            print(
                f"{column} → Bar Chart"
            )

        print("\nBINARY")
        print("-" * 80)

        for column in groups["binary"]:

            print(
                f"{column} → Bar Chart"
            )

        print("\nCATEGORICAL")
        print("-" * 80)

        for column in groups["categorical"]:

            print(
                f"{column} → Bar Chart"
            )

        print("\nHIGH CARDINALITY")
        print("-" * 80)

        for column in groups[
            "high_cardinality"
        ]:

            print(
                f"{column} → Skipped"
            )

        print("\nID COLUMNS")
        print("-" * 80)

        for column in groups["id"]:

            print(
                f"{column} → Skipped"
            )

        print("=" * 80)
        # ==================================================
    # Generate All Smart Visualizations
    # ==================================================

    def generate_all(
        self,
        top_n=15
    ):
        """
        Automatically generate appropriate
        visualizations based on column profiles.
        """

        self._check_data()

        print("\n")
        print("=" * 70)
        print("           DATAMOP SMART VISUALIZATION ENGINE")
        print("=" * 70)

        # ----------------------------------------------
        # Show visualization decisions
        # ----------------------------------------------

        self.display_visualization_plan()

        # ----------------------------------------------
        # Numerical Visualizations
        # ----------------------------------------------

        print(
            "\nGenerating continuous numerical "
            "visualizations..."
        )

        self.generate_numerical_visualizations()

        # ----------------------------------------------
        # Categorical Visualizations
        # ----------------------------------------------

        print(
            "Generating categorical "
            "visualizations..."
        )

        self.generate_categorical_visualizations(
            top_n=top_n
        )

        # ----------------------------------------------
        # Missing Values
        # ----------------------------------------------

        print(
            "Generating missing-value "
            "visualization..."
        )

        self.missing_value_chart()

        # ----------------------------------------------
        # Correlation
        # ----------------------------------------------

        print(
            "Generating correlation heatmap..."
        )

        self.correlation_heatmap()

        # ----------------------------------------------
        # Final
        # ----------------------------------------------

        print(
            "\nSmart visualization generation "
            "completed."
        )

        print(
            f"Charts generated: "
            f"{len(self.generated_files)}"
        )

        print(
            f"Output folder: "
            f"{self.output_dir}"
        )

        print("=" * 70)

        return self.generated_files
    # ==================================================
    # Get Generated Files
    # ==================================================

    def get_generated_files(self):
        """
        Return generated visualization files.
        """

        return self.generated_files.copy()