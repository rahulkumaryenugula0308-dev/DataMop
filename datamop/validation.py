"""
DataMop - Input Validation

Validates files, DataFrames and DataMop parameters
before processing begins.
"""

import os

import pandas as pd

from datamop.exceptions import (
    DataMopInputError,
    DataMopFileError,
    DataMopDataError,
    DataMopConfigurationError
)


class DataValidator:
    """
    Central validation engine for DataMop.
    """

    SUPPORTED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".xls"
    }

    # ==================================================
    # Validate Dataset Input
    # ==================================================

    @classmethod
    def validate_input(cls, data):
        """
        Validate DataFrame or file path.
        """

        # ----------------------------------------------
        # DataFrame
        # ----------------------------------------------

        if isinstance(
            data,
            pd.DataFrame
        ):

            cls.validate_dataframe(
                data
            )

            return "dataframe"

        # ----------------------------------------------
        # File Path
        # ----------------------------------------------

        if isinstance(
            data,
            (str, os.PathLike)
        ):

            filepath = os.fspath(
                data
            )

            cls.validate_file(
                filepath
            )

            return "file"

        raise DataMopInputError(
            "Input must be either:\n"
            "1. A pandas DataFrame\n"
            "2. A CSV or Excel file path."
        )

    # ==================================================
    # Validate File
    # ==================================================

    @classmethod
    def validate_file(cls, filepath):
        """
        Validate dataset file.
        """

        if not filepath:

            raise DataMopFileError(
                "No file path was provided."
            )

        if not os.path.exists(
            filepath
        ):

            raise DataMopFileError(
                f"Dataset file not found:\n"
                f"{filepath}"
            )

        if not os.path.isfile(
            filepath
        ):

            raise DataMopFileError(
                f"The specified path is not a file:\n"
                f"{filepath}"
            )

        extension = (
            os.path.splitext(
                filepath
            )[1]
            .lower()
        )

        if extension not in (
            cls.SUPPORTED_EXTENSIONS
        ):

            supported = ", ".join(
                sorted(
                    cls.SUPPORTED_EXTENSIONS
                )
            )

            raise DataMopFileError(
                f"Unsupported file format: "
                f"'{extension}'\n"
                f"Supported formats: "
                f"{supported}"
            )

        return True

    # ==================================================
    # Validate DataFrame
    # ==================================================

    @classmethod
    def validate_dataframe(
        cls,
        dataframe
    ):
        """
        Validate pandas DataFrame.
        """

        if not isinstance(
            dataframe,
            pd.DataFrame
        ):

            raise DataMopInputError(
                "Expected a pandas DataFrame."
            )

        if dataframe.empty:

            raise DataMopDataError(
                "The supplied DataFrame is empty.\n"
                "Please provide a dataset containing "
                "at least one row."
            )

        if len(
            dataframe.columns
        ) == 0:

            raise DataMopDataError(
                "The supplied DataFrame has no columns."
            )

        # Check duplicate column names

        if dataframe.columns.duplicated().any():

            duplicated = (
                dataframe.columns[
                    dataframe.columns.duplicated()
                ]
                .tolist()
            )

            raise DataMopDataError(
                "Duplicate column names detected:\n"
                f"{duplicated}"
            )

        return True

    # ==================================================
    # Validate Outlier Method
    # ==================================================

    @classmethod
    def validate_outlier_method(
        cls,
        method
    ):
        """
        Validate outlier detection method.
        """

        if not isinstance(
            method,
            str
        ):

            raise DataMopConfigurationError(
                "Outlier method must be a string."
            )

        method = method.lower().strip()

        if method not in {
            "iqr",
            "zscore"
        }:

            raise DataMopConfigurationError(
                "Invalid outlier method.\n"
                "Choose either 'iqr' or 'zscore'."
            )

        return method

    # ==================================================
    # Validate Threshold
    # ==================================================

    @classmethod
    def validate_threshold(
        cls,
        threshold,
        name="threshold",
        minimum=0,
        maximum=None
    ):
        """
        Validate numerical threshold.
        """

        if not isinstance(
            threshold,
            (int, float)
        ):

            raise DataMopConfigurationError(
                f"{name} must be a number."
            )

        if threshold < minimum:

            raise DataMopConfigurationError(
                f"{name} must be >= {minimum}."
            )

        if (
            maximum is not None
            and threshold > maximum
        ):

            raise DataMopConfigurationError(
                f"{name} must be <= {maximum}."
            )

        return True