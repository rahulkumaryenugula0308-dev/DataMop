"""
DataMop - Duplicate Handler

This module detects, analyzes, and removes duplicate
records from pandas DataFrames.
"""

import pandas as pd


class DuplicateHandler:
    """
    Class for detecting and handling duplicate rows.
    """

    def __init__(self, dataframe=None):
        """
        Initialize DuplicateHandler.

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
        Set the DataFrame for duplicate processing.
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
    # Count Duplicates
    # ==================================================

    def count_duplicates(self, subset=None):
        """
        Count duplicate rows.

        Parameters
        ----------
        subset : list, optional
            Columns to consider when identifying duplicates.

        Returns
        -------
        int
            Number of duplicate rows.
        """

        self._check_data()

        return int(
            self.df.duplicated(
                subset=subset,
                keep="first"
            ).sum()
        )

    # ==================================================
    # Duplicate Percentage
    # ==================================================

    def duplicate_percentage(self, subset=None):
        """
        Calculate percentage of duplicate rows.
        """

        self._check_data()

        if len(self.df) == 0:
            return 0.0

        duplicate_count = self.count_duplicates(
            subset=subset
        )

        percentage = (
            duplicate_count / len(self.df)
        ) * 100

        return round(percentage, 2)

    # ==================================================
    # Detect Duplicates
    # ==================================================

    def detect(self, subset=None):
        """
        Return a boolean Series identifying duplicate rows.
        """

        self._check_data()

        return self.df.duplicated(
            subset=subset,
            keep="first"
        )

    # ==================================================
    # Get Duplicate Rows
    # ==================================================

    def get_duplicates(self, subset=None):
        """
        Return duplicate rows.

        The first occurrence is considered valid,
        and subsequent occurrences are returned.
        """

        self._check_data()

        duplicate_mask = self.df.duplicated(
            subset=subset,
            keep="first"
        )

        return self.df[duplicate_mask].copy()

    # ==================================================
    # Get All Duplicate Groups
    # ==================================================

    def get_all_duplicate_records(self, subset=None):
        """
        Return all records that belong to duplicate groups.

        Unlike get_duplicates(), this also includes
        the first occurrence.
        """

        self._check_data()

        duplicate_mask = self.df.duplicated(
            subset=subset,
            keep=False
        )

        return self.df[duplicate_mask].copy()

    # ==================================================
    # Remove Duplicates
    # ==================================================

    def remove_duplicates(
        self,
        subset=None,
        keep="first"
    ):
        """
        Remove duplicate rows.

        Parameters
        ----------
        subset : list, optional
            Columns used to identify duplicates.

        keep : str
            'first', 'last', or False.

        Returns
        -------
        pandas.DataFrame
            Cleaned DataFrame.
        """

        self._check_data()

        if keep not in ["first", "last", False]:
            raise ValueError(
                "keep must be 'first', 'last', or False."
            )

        before = len(self.df)

        duplicate_count = self.count_duplicates(
            subset=subset
        )

        self.df = self.df.drop_duplicates(
            subset=subset,
            keep=keep
        ).reset_index(drop=True)

        after = len(self.df)

        removed = before - after

        self.logs.append(
            f"Removed {removed} duplicate rows "
            f"using keep='{keep}'."
        )

        return self.df

    # ==================================================
    # Remove Duplicates by Columns
    # ==================================================

    def remove_duplicates_by_columns(
        self,
        columns,
        keep="first"
    ):
        """
        Remove duplicates based on selected columns.

        Example:
            remove_duplicates_by_columns(
                ["Name", "Age"]
            )
        """

        self._check_data()

        if not columns:
            raise ValueError(
                "At least one column must be provided."
            )

        missing_columns = [
            column
            for column in columns
            if column not in self.df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Columns not found: {missing_columns}"
            )

        before = len(self.df)

        self.df = self.df.drop_duplicates(
            subset=columns,
            keep=keep
        ).reset_index(drop=True)

        removed = before - len(self.df)

        self.logs.append(
            f"Removed {removed} duplicates based on "
            f"columns: {columns}."
        )

        return self.df

    # ==================================================
    # Remove All Duplicate Records
    # ==================================================

    def remove_all_duplicate_records(
        self,
        subset=None
    ):
        """
        Remove every record belonging to a duplicate group.

        Example:

        A
        A
        B

        becomes:

        B
        """

        self._check_data()

        before = len(self.df)

        duplicate_mask = self.df.duplicated(
            subset=subset,
            keep=False
        )

        duplicate_count = int(
            duplicate_mask.sum()
        )

        self.df = self.df[
            ~duplicate_mask
        ].reset_index(drop=True)

        self.logs.append(
            f"Removed {duplicate_count} rows belonging "
            f"to duplicate groups."
        )

        return self.df

    # ==================================================
    # Display Report
    # ==================================================

    def display_report(self, subset=None):
        """
        Display duplicate information.
        """

        self._check_data()

        total_rows = len(self.df)

        duplicate_count = self.count_duplicates(
            subset=subset
        )

        percentage = self.duplicate_percentage(
            subset=subset
        )

        print("\n")
        print("=" * 70)
        print("                 DATAMOP DUPLICATE REPORT")
        print("=" * 70)

        print(
            f"\nTotal Rows          : {total_rows}"
        )

        print(
            f"Duplicate Rows      : {duplicate_count}"
        )

        print(
            f"Duplicate Percentage : {percentage}%"
        )

        print("\n" + "=" * 70)

    # ==================================================
    # Display Duplicate Rows
    # ==================================================

    def display_duplicates(self, subset=None):
        """
        Display duplicate records.
        """

        self._check_data()

        duplicates = self.get_duplicates(
            subset=subset
        )

        print("\n")
        print("=" * 70)
        print("                 DUPLICATE RECORDS")
        print("=" * 70)

        if duplicates.empty:

            print("No duplicate rows found.")

        else:

            print(
                duplicates.to_string(
                    index=False
                )
            )

        print("=" * 70)

    # ==================================================
    # Cleaning Log
    # ==================================================

    def get_log(self):
        """
        Return duplicate handling log.
        """

        return self.logs

    def display_log(self):
        """
        Display duplicate handling operations.
        """

        print("\n")
        print("=" * 70)
        print("                 DUPLICATE CLEANING LOG")
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