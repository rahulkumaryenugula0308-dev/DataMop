"""
DataMop - Data Type Handler

This module detects, analyzes, and converts data types
in pandas DataFrames.
"""

import pandas as pd
import numpy as np


class DataTypeHandler:
    """
    Detect and convert data types in a DataFrame.
    """

    def __init__(self, dataframe=None):
        """
        Initialize DataTypeHandler.
        """

        self.df = dataframe
        self.logs = []

    # ==================================================
    # Set Data
    # ==================================================

    def set_data(self, dataframe):
        """
        Set the DataFrame for processing.
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
    # Get Data Types
    # ==================================================

    def get_data_types(self):
        """
        Return data types of all columns.
        """

        self._check_data()

        return self.df.dtypes

    # ==================================================
    # Data Type Report
    # ==================================================

    def get_type_report(self):
        """
        Generate detailed data type report.
        """

        self._check_data()

        report = []

        for column in self.df.columns:

            dtype = self.df[column].dtype

            report.append({
                "column": column,
                "data_type": str(dtype),
                "non_null": int(
                    self.df[column].notna().sum()
                ),
                "missing": int(
                    self.df[column].isna().sum()
                ),
                "unique_values": int(
                    self.df[column].nunique(
                        dropna=False
                    )
                )
            })

        return pd.DataFrame(report)

    # ==================================================
    # Numeric Columns
    # ==================================================

    def get_numeric_columns(self):
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
        Return categorical/text columns.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=[
                "object",
                "category",
                "string"
            ]
        ).columns.tolist()

    # ==================================================
    # Datetime Columns
    # ==================================================

    def get_datetime_columns(self):
        """
        Return datetime columns.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=[
                "datetime",
                "datetimetz"
            ]
        ).columns.tolist()

    # ==================================================
    # Boolean Columns
    # ==================================================

    def get_boolean_columns(self):
        """
        Return boolean columns.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=["bool"]
        ).columns.tolist()

    # ==================================================
    # Convert Numeric Column
    # ==================================================

    def convert_to_numeric(
        self,
        columns=None,
        errors="coerce"
    ):
        """
        Convert columns to numeric.

        Parameters
        ----------
        columns : list, optional
            Columns to convert.

        errors : str
            'raise', 'coerce', or 'ignore'.
        """

        self._check_data()

        if columns is None:
            columns = self.get_categorical_columns()

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            old_type = str(
                self.df[column].dtype
            )

            self.df[column] = pd.to_numeric(
                self.df[column],
                errors=errors
            )

            new_type = str(
                self.df[column].dtype
            )

            self.logs.append(
                f"Converted '{column}' "
                f"from {old_type} to {new_type}."
            )

        return self.df

    # ==================================================
    # Convert Datetime
    # ==================================================

    def convert_to_datetime(
        self,
        columns,
        errors="coerce"
    ):
        """
        Convert columns to datetime.
        """

        self._check_data()

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            old_type = str(
                self.df[column].dtype
            )

            self.df[column] = pd.to_datetime(
                self.df[column],
                errors=errors
            )

            new_type = str(
                self.df[column].dtype
            )

            self.logs.append(
                f"Converted '{column}' "
                f"from {old_type} to {new_type}."
            )

        return self.df

    # ==================================================
    # Convert Category
    # ==================================================

    def convert_to_category(
        self,
        columns
    ):
        """
        Convert columns to pandas category type.
        """

        self._check_data()

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            old_type = str(
                self.df[column].dtype
            )

            self.df[column] = (
                self.df[column].astype("category")
            )

            self.logs.append(
                f"Converted '{column}' "
                f"from {old_type} to category."
            )

        return self.df

    # ==================================================
    # Convert Boolean
    # ==================================================

    def convert_to_boolean(
        self,
        columns
    ):
        """
        Convert columns to boolean.

        Recognizes:
            True / False
            Yes / No
            Y / N
            1 / 0
        """

        self._check_data()

        true_values = {
            "true",
            "yes",
            "y",
            "1",
            "t"
        }

        false_values = {
            "false",
            "no",
            "n",
            "0",
            "f"
        }

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            old_type = str(
                self.df[column].dtype
            )

            def convert_value(value):

                if pd.isna(value):
                    return np.nan

                value_str = str(
                    value
                ).strip().lower()

                if value_str in true_values:
                    return True

                if value_str in false_values:
                    return False

                return np.nan

            self.df[column] = (
                self.df[column]
                .apply(convert_value)
                .astype("boolean")
            )

            self.logs.append(
                f"Converted '{column}' "
                f"from {old_type} to boolean."
            )

        return self.df

    # ==================================================
    # Detect Potential Numeric Columns
    # ==================================================

    def detect_numeric_candidates(
        self,
        threshold=0.80
    ):
        """
        Detect object columns that are mostly numeric.

        Example:

            "100"
            "200"
            "300"
            "unknown"

        If the percentage of convertible values is above
        the threshold, the column is considered a numeric
        candidate.
        """

        self._check_data()

        candidates = []

        categorical_columns = (
            self.get_categorical_columns()
        )

        for column in categorical_columns:

            converted = pd.to_numeric(
                self.df[column],
                errors="coerce"
            )

            valid_count = converted.notna().sum()

            total_count = self.df[column].notna().sum()

            if total_count == 0:
                continue

            ratio = valid_count / total_count

            if ratio >= threshold:

                candidates.append({
                    "column": column,
                    "convertible_percentage":
                        round(ratio * 100, 2)
                })

        return pd.DataFrame(candidates)

    
    # ==================================================
    # Detect Potential Datetime Columns
    # ==================================================

    def detect_datetime_candidates(
        self,
        threshold=0.80
    ):
        """
        Detect object columns that are likely to contain dates.

        Only columns containing values that strongly resemble
        date strings are tested for datetime conversion.
        """

        self._check_data()

        candidates = []

        categorical_columns = (
            self.get_categorical_columns()
        )

        for column in categorical_columns:

            series = self.df[column].dropna()

            if series.empty:
                continue

            # Convert values to strings
            values = series.astype(str).str.strip()

            # Check whether values look like dates.
            date_pattern = values.str.contains(
                r"^\d{4}[-/]\d{1,2}[-/]\d{1,4}$"
                r"|"
                r"^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}$",
                regex=True,
                na=False
            )

            date_like_ratio = (
                date_pattern.mean()
            )

            # If most values don't look like dates,
            # skip this column.
            if date_like_ratio < threshold:
                continue

            # Only attempt datetime conversion on
            # values that actually look like dates.
            converted = pd.to_datetime(
                values.where(date_pattern),
                errors="coerce"
            )

            valid_count = (
                converted.notna().sum()
            )

            total_count = len(values)

            if total_count == 0:
                continue

            ratio = (
                valid_count / total_count
            )

            if ratio >= threshold:

                candidates.append({
                    "column": column,
                    "convertible_percentage":
                        round(
                            ratio * 100,
                            2
                        )
                })

        return pd.DataFrame(candidates)

    # ==================================================
    # Automatic Type Conversion
    # ==================================================

    def auto_convert(
        self,
        numeric_threshold=0.90,
        datetime_threshold=0.90
    ):
        """
        Automatically convert obvious data types.

        Order:
            1. Numeric candidates
            2. Datetime candidates
        """

        self._check_data()

        # Numeric candidates
        numeric_candidates = (
            self.detect_numeric_candidates(
                threshold=numeric_threshold
            )
        )

        for _, row in numeric_candidates.iterrows():

            column = row["column"]

            self.df[column] = pd.to_numeric(
                self.df[column],
                errors="coerce"
            )

            self.logs.append(
                f"Automatically converted "
                f"'{column}' to numeric."
            )

        # Datetime candidates
        datetime_candidates = (
            self.detect_datetime_candidates(
                threshold=datetime_threshold
            )
        )

        for _, row in datetime_candidates.iterrows():

            column = row["column"]

            # Only convert columns that are
            # still object/category/string
            if column in self.df.columns:

                if (
                    self.df[column].dtype
                    == "object"
                    or
                    str(
                        self.df[column].dtype
                    ) == "string"
                ):

                    self.df[column] = (
                        pd.to_datetime(
                            self.df[column],
                            errors="coerce"
                        )
                    )

                    self.logs.append(
                        f"Automatically converted "
                        f"'{column}' to datetime."
                    )

        return self.df

    # ==================================================
    # Display Report
    # ==================================================

    def display_report(self):
        """
        Display data type report.
        """

        self._check_data()

        print("\n")
        print("=" * 80)
        print("                  DATAMOP DATA TYPE REPORT")
        print("=" * 80)

        print("\nCURRENT DATA TYPES")
        print("-" * 80)

        print(
            self.get_type_report().to_string(
                index=False
            )
        )

        print("\nNUMERICAL COLUMNS")
        print("-" * 80)

        numeric = self.get_numeric_columns()

        if numeric:
            print(", ".join(numeric))
        else:
            print("None")

        print("\nCATEGORICAL COLUMNS")
        print("-" * 80)

        categorical = (
            self.get_categorical_columns()
        )

        if categorical:
            print(", ".join(categorical))
        else:
            print("None")

        print("\nDATETIME COLUMNS")
        print("-" * 80)

        datetime_columns = (
            self.get_datetime_columns()
        )

        if datetime_columns:
            print(
                ", ".join(
                    datetime_columns
                )
            )
        else:
            print("None")

        print("\nBOOLEAN COLUMNS")
        print("-" * 80)

        boolean_columns = (
            self.get_boolean_columns()
        )

        if boolean_columns:
            print(
                ", ".join(
                    boolean_columns
                )
            )
        else:
            print("None")

        print("=" * 80)

    # ==================================================
    # Display Log
    # ==================================================

    def get_log(self):
        """
        Return conversion log.
        """

        return self.logs

    def display_log(self):
        """
        Display all type conversion operations.
        """

        print("\n")
        print("=" * 80)
        print("                  DATA TYPE LOG")
        print("=" * 80)

        if not self.logs:

            print("No conversions performed.")

        else:

            for number, log in enumerate(
                self.logs,
                start=1
            ):

                print(
                    f"{number}. {log}"
                )

        print("=" * 80) 