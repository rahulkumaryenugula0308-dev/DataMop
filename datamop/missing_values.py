"""
DataMop - Missing Value Handler

This module detects, analyzes, and handles missing values
in pandas DataFrames.
"""

import pandas as pd
import numpy as np


class MissingValueHandler:
    """
    Class for detecting and handling missing values.
    """

    def __init__(self, dataframe=None):
        """
        Initialize the MissingValueHandler.

        Parameters
        ----------
        dataframe : pandas.DataFrame, optional
            Dataset to process.
        """

        self.df = dataframe
        self.logs = []

    # ==================================================
    # Set Data
    # ==================================================

    def set_data(self, dataframe):
        """
        Set the DataFrame to process.
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
        Check whether a DataFrame is available.
        """

        if self.df is None:
            raise ValueError(
                "No dataset available. "
                "Set or load a dataset first."
            )

    # ==================================================
    # Validate Threshold
    # ==================================================

    def _validate_threshold(self, missing_threshold):
        """
        Validate the missing-column threshold.

        Parameters
        ----------
        missing_threshold : float
            Percentage between 0 and 100.
        """

        if not isinstance(
            missing_threshold,
            (int, float)
        ):
            raise TypeError(
                "missing_threshold must be a number."
            )

        if missing_threshold < 0 or missing_threshold > 100:
            raise ValueError(
                "missing_threshold must be between "
                "0 and 100."
            )

    # ==================================================
    # Detect Missing Values
    # ==================================================

    def detect(self):
        """
        Detect missing values in every column.

        Returns
        -------
        pandas.DataFrame
            Missing-value report.
        """

        self._check_data()

        if len(self.df) == 0:

            return pd.DataFrame({
                "column": self.df.columns,
                "missing_count": 0,
                "missing_percentage": 0.0,
                "data_type": [
                    str(self.df[column].dtype)
                    for column in self.df.columns
                ]
            })

        missing_count = self.df.isnull().sum()

        missing_percentage = (
            missing_count / len(self.df)
        ) * 100

        report = pd.DataFrame({
            "column": self.df.columns,
            "missing_count": missing_count.values,
            "missing_percentage": missing_percentage.values
        })

        report["data_type"] = [
            str(self.df[column].dtype)
            for column in self.df.columns
        ]

        return report.sort_values(
            by="missing_percentage",
            ascending=False
        ).reset_index(drop=True)

    # ==================================================
    # Get Columns With Missing Values
    # ==================================================

    def columns_with_missing_values(self):
        """
        Return columns containing missing values.
        """

        self._check_data()

        return self.df.columns[
            self.df.isnull().any()
        ].tolist()

    # ==================================================
    # Get Total Missing Values
    # ==================================================

    def total_missing_values(self):
        """
        Return total number of missing cells.
        """

        self._check_data()

        return int(
            self.df.isnull().sum().sum()
        )

    # ==================================================
    # Missing Value Percentage
    # ==================================================

    def missing_percentage(self):
        """
        Return overall missing-value percentage.
        """

        self._check_data()

        total_cells = (
            self.df.shape[0] *
            self.df.shape[1]
        )

        if total_cells == 0:
            return 0.0

        missing_cells = self.total_missing_values()

        percentage = (
            missing_cells / total_cells
        ) * 100

        return round(percentage, 2)

    # ==================================================
    # Drop Columns With High Missing Percentage
    # ==================================================

    def drop_high_missing_columns(
        self,
        missing_threshold=40
    ):
        """
        Automatically remove columns whose missing-value
        percentage is greater than the threshold.

        Example
        -------
        missing_threshold=40

        25% missing -> keep column
        40% missing -> keep column
        41% missing -> remove column
        """

        self._check_data()

        self._validate_threshold(
            missing_threshold
        )

        if len(self.df) == 0:
            return self.df

        missing_percentages = (
            self.df.isnull().mean() * 100
        )

        columns_to_drop = (
            missing_percentages[
                missing_percentages > missing_threshold
            ]
            .index
            .tolist()
        )

        if columns_to_drop:

            missing_details = []

            for column in columns_to_drop:

                percentage = round(
                    float(
                        missing_percentages[column]
                    ),
                    2
                )

                missing_details.append(
                    f"{column} ({percentage}%)"
                )

            self.df = self.df.drop(
                columns=columns_to_drop
            )

            self.logs.append(
                "Dropped columns with more than "
                f"{missing_threshold}% missing values: "
                + ", ".join(missing_details)
            )

        else:

            self.logs.append(
                "No columns exceeded the "
                f"{missing_threshold}% missing-value threshold."
            )

        return self.df

    # ==================================================
    # Fill Numerical Columns
    # ==================================================

    def fill_numeric(
        self,
        strategy="median",
        value=None
    ):
        """
        Fill missing values in numerical columns.

        Parameters
        ----------
        strategy : str
            'mean', 'median', or 'value'

        value : numeric, optional
            Custom value when strategy='value'.
        """

        self._check_data()

        numeric_columns = self.df.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:

            missing_count = int(
                self.df[column].isnull().sum()
            )

            if missing_count == 0:
                continue

            if strategy == "mean":

                fill_value = self.df[column].mean()

            elif strategy == "median":

                fill_value = self.df[column].median()

            elif strategy == "value":

                if value is None:
                    raise ValueError(
                        "Provide a value when "
                        "using strategy='value'."
                    )

                fill_value = value

            else:

                raise ValueError(
                    "Invalid strategy. Use "
                    "'mean', 'median', or 'value'."
                )

            self.df[column] = self.df[column].fillna(
                fill_value
            )

            self.logs.append(
                f"Filled {missing_count} missing values "
                f"in '{column}' using {strategy}."
            )

        return self.df

    # ==================================================
    # Fill Categorical Columns
    # ==================================================

    def fill_categorical(
        self,
        strategy="mode",
        value=None
    ):
        """
        Fill missing values in categorical columns.

        Parameters
        ----------
        strategy : str
            'mode' or 'value'

        value : str, optional
            Custom value when strategy='value'.
        """

        self._check_data()

        categorical_columns = self.df.select_dtypes(
            include=[
                "object",
                "category",
                "string"
            ]
        ).columns

        for column in categorical_columns:

            missing_count = int(
                self.df[column].isnull().sum()
            )

            if missing_count == 0:
                continue

            if strategy == "mode":

                mode_values = self.df[column].mode()

                if len(mode_values) == 0:
                    continue

                fill_value = mode_values.iloc[0]

            elif strategy == "value":

                if value is None:
                    raise ValueError(
                        "Provide a value when "
                        "using strategy='value'."
                    )

                fill_value = value

            else:

                raise ValueError(
                    "Invalid strategy. Use "
                    "'mode' or 'value'."
                )

            self.df[column] = self.df[column].fillna(
                fill_value
            )

            self.logs.append(
                f"Filled {missing_count} missing values "
                f"in '{column}' using {strategy}."
            )

        return self.df

    # ==================================================
    # Drop Rows
    # ==================================================

    def drop_rows(self, threshold=None):
        """
        Drop rows containing missing values.

        Parameters
        ----------
        threshold : int, optional
            Minimum number of non-null values required
            for a row to remain.
        """

        self._check_data()

        before = len(self.df)

        if threshold is None:

            self.df = self.df.dropna()

        else:

            self.df = self.df.dropna(
                thresh=threshold
            )

        after = len(self.df)

        removed = before - after

        self.logs.append(
            f"Removed {removed} rows containing "
            f"missing values."
        )

        return self.df

    # ==================================================
    # Drop Specific Columns
    # ==================================================

    def drop_columns(
        self,
        columns=None,
        missing_threshold=50
    ):
        """
        Drop specific columns or columns having excessive
        missing values.

        Parameters
        ----------
        columns : list, optional
            Specific columns to remove.

        missing_threshold : float
            Percentage threshold.
        """

        self._check_data()

        self._validate_threshold(
            missing_threshold
        )

        if columns is not None:

            existing_columns = [
                column
                for column in columns
                if column in self.df.columns
            ]

            if existing_columns:

                self.df = self.df.drop(
                    columns=existing_columns
                )

                self.logs.append(
                    f"Removed columns: "
                    f"{existing_columns}"
                )

            return self.df

        return self.drop_high_missing_columns(
            missing_threshold=missing_threshold
        )

    # ==================================================
    # Automatic Handling
    # ==================================================

    def auto_fill(
        self,
        missing_threshold=40
    ):
        """
        Automatically handle missing values.

        Rule
        ----
        Columns with more than the configured missing
        percentage are removed first.

        Default:
            40%

        Numerical columns:
            Median

        Categorical columns:
            Mode

        Example
        -------
        35% missing -> fill
        40% missing -> fill
        45% missing -> drop
        """

        self._check_data()

        self._validate_threshold(
            missing_threshold
        )

        # ----------------------------------------------
        # Step 1: Remove columns with excessive missing
        # values before performing imputation.
        # ----------------------------------------------

        self.drop_high_missing_columns(
            missing_threshold=missing_threshold
        )

        # ----------------------------------------------
        # Step 2: Fill remaining numerical columns
        # ----------------------------------------------

        self.fill_numeric(
            strategy="median"
        )

        # ----------------------------------------------
        # Step 3: Fill remaining categorical columns
        # ----------------------------------------------

        self.fill_categorical(
            strategy="mode"
        )

        self.logs.append(
            "Automatic missing-value handling completed "
            f"with a {missing_threshold}% column threshold."
        )

        return self.df

    # ==================================================
    # Display Report
    # ==================================================

    def display_report(self):
        """
        Display a missing-value report.
        """

        self._check_data()

        report = self.detect()

        print("\n")
        print("=" * 70)
        print("              DATAMOP MISSING VALUE REPORT")
        print("=" * 70)

        print(
            f"\nTotal Missing Cells : "
            f"{self.total_missing_values()}"
        )

        print(
            f"Overall Missing %  : "
            f"{self.missing_percentage()}%"
        )

        print("\nColumn-wise Missing Values")
        print("-" * 70)

        if report.empty:

            print("No columns found.")

        else:

            print(
                report.to_string(
                    index=False
                )
            )

        print("\n" + "=" * 70)

    # ==================================================
    # Cleaning Log
    # ==================================================

    def get_log(self):
        """
        Return the list of operations performed.
        """

        return self.logs

    def display_log(self):
        """
        Display all operations performed.
        """

        print("\n")
        print("=" * 70)
        print("              MISSING VALUE LOG")
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