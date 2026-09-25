"""
DataMop - Text Standardization Handler

This module standardizes text and categorical columns
in pandas DataFrames.
"""

import pandas as pd


class TextStandardizer:
    """
    Standardize text and categorical values in a DataFrame.
    """

    def __init__(self, dataframe=None):
        """
        Initialize TextStandardizer.
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
    # Get Text Columns
    # ==================================================

    def get_text_columns(self):
        """
        Return text and categorical columns.
        """

        self._check_data()

        return self.df.select_dtypes(
            include=[
                "object",
                "string",
                "category"
            ]
        ).columns.tolist()

    # ==================================================
    # Trim Whitespace
    # ==================================================

    def trim_whitespace(
        self,
        columns=None
    ):
        """
        Remove leading and trailing whitespace
        from text values.
        """

        self._check_data()

        if columns is None:
            columns = self.get_text_columns()

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            if (
                self.df[column].dtype
                == "object"
                or
                str(self.df[column].dtype)
                == "string"
                or
                str(self.df[column].dtype)
                == "category"
            ):

                before = (
                    self.df[column]
                    .astype("string")
                )

                after = before.str.strip()

                changed = int(
                    (
                        before.fillna("")
                        != after.fillna("")
                    ).sum()
                )

                self.df[column] = after

                self.logs.append({
                    "operation":
                        "TRIM_WHITESPACE",
                    "column":
                        column,
                    "values_changed":
                        changed,
                    "status":
                        "SUCCESS"
                })

        return self.df

    # ==================================================
    # Standardize Case
    # ==================================================

    def standardize_case(
        self,
        columns=None,
        case="lower"
    ):
        """
        Standardize text case.

        Supported cases:
            lower
            upper
            title
        """

        self._check_data()

        if case not in {
            "lower",
            "upper",
            "title"
        }:
            raise ValueError(
                "case must be 'lower', "
                "'upper', or 'title'."
            )

        if columns is None:
            columns = self.get_text_columns()

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            series = (
                self.df[column]
                .astype("string")
            )

            if case == "lower":

                standardized = series.str.lower()

            elif case == "upper":

                standardized = series.str.upper()

            else:

                standardized = series.str.title()

            changed = int(
                (
                    series.fillna("")
                    != standardized.fillna("")
                ).sum()
            )

            self.df[column] = standardized

            self.logs.append({
                "operation":
                    "STANDARDIZE_CASE",
                "column":
                    column,
                "case":
                    case,
                "values_changed":
                    changed,
                "status":
                    "SUCCESS"
            })

        return self.df

    # ==================================================
    # Normalize Category Labels
    # ==================================================

    def normalize_categories(
        self,
        columns=None
    ):
        """
        Normalize categorical labels.

        The method trims whitespace and standardizes
        case before grouping equivalent labels.

        Examples:

            Male
            male
            MALE
            Male

        become:

            male
        """

        self._check_data()

        if columns is None:
            columns = self.get_text_columns()

        for column in columns:

            if column not in self.df.columns:
                raise ValueError(
                    f"Column '{column}' not found."
                )

            series = (
                self.df[column]
                .astype("string")
            )

            standardized = (
                series
                .str.strip()
                .str.lower()
            )

            changed = int(
                (
                    series.fillna("")
                    != standardized.fillna("")
                ).sum()
            )

            self.df[column] = standardized

            self.logs.append({
                "operation":
                    "NORMALIZE_CATEGORIES",
                "column":
                    column,
                "values_changed":
                    changed,
                "status":
                    "SUCCESS"
            })

        return self.df

    # ==================================================
    # Complete Text Standardization
    # ==================================================

    def standardize(
        self,
        columns=None,
        case="lower",
        normalize_categories=True
    ):
        """
        Run complete text standardization.

        Steps:
            1. Trim whitespace
            2. Standardize case
            3. Normalize category labels
        """

        self._check_data()

        if columns is None:
            columns = self.get_text_columns()

        if not columns:
            return self.df

        # ----------------------------------------------
        # Trim whitespace
        # ----------------------------------------------

        self.trim_whitespace(
            columns=columns
        )

        # ----------------------------------------------
        # Standardize case
        # ----------------------------------------------

        self.standardize_case(
            columns=columns,
            case=case
        )

        # ----------------------------------------------
        # Normalize categories
        # ----------------------------------------------

        if normalize_categories:

            self.normalize_categories(
                columns=columns
            )

        return self.df

    # ==================================================
    # Get Log
    # ==================================================

    def get_log(self):
        """
        Return standardization logs.
        """

        return self.logs

    # ==================================================
    # Display Log
    # ==================================================

    def display_log(self):
        """
        Display text standardization operations.
        """

        print("\n")
        print("=" * 80)
        print(
            "              TEXT STANDARDIZATION LOG"
        )
        print("=" * 80)

        if not self.logs:

            print(
                
                "No text standardization operations performed."
            )

        else:

            for number, log in enumerate(
                self.logs,
                start=1
            ):

                print(
                    f"{number}. {log}"
                )

        print("=" * 80)