"""
DataMop - Main Data Cleaning Controller

This module integrates all DataMop components into
a single easy-to-use DataCleaner class.
"""

import pandas as pd

from datamop.loader import DataLoader
from datamop.analyzer import DataAnalyzer
from datamop.missing_values import MissingValueHandler
from datamop.duplicates import DuplicateHandler
from datamop.outliers import OutlierHandler
from datamop.datatype import DataTypeHandler
from datamop.text_standardization import TextStandardizer
from datamop.logger import DataLogger


class DataCleaner:
    """
    Main controller for the DataMop data-cleaning pipeline.
    """

    def __init__(self):
        """Initialize all DataMop components."""

        self.df = None
        self.filepath = None

        self.loader = DataLoader()
        self.analyzer = None
        self.missing_handler = None
        self.duplicate_handler = None
        self.outlier_handler = None
        self.datatype_handler = None
        self.text_standardizer = None

        self.logger = DataLogger()

    # ==================================================
    # Load
    # ==================================================

    def load(self, filepath):
        """Load a CSV or Excel dataset."""

        self.df = self.loader.load(filepath)
        self.filepath = filepath

        self.analyzer = DataAnalyzer(self.df)
        self.missing_handler = MissingValueHandler(self.df)
        self.duplicate_handler = DuplicateHandler(self.df)
        self.outlier_handler = OutlierHandler(self.df)
        self.datatype_handler = DataTypeHandler(self.df)
        self.text_standardizer = TextStandardizer(self.df)

        self.logger.success(
            module="LOADER",
            operation="LOAD_DATASET",
            description=(
                f"Dataset loaded successfully from {filepath}."
            ),
            rows_affected=len(self.df),
            columns_affected=len(self.df.columns)
        )

        return self.df

    # ==================================================
    # Synchronize Data
    # ==================================================

    def _sync_handlers(self):
        """Synchronize the current DataFrame with all handlers."""

        if self.df is None:
            raise ValueError("No dataset loaded.")

        self.analyzer.set_data(self.df)
        self.missing_handler.set_data(self.df)
        self.duplicate_handler.set_data(self.df)
        self.outlier_handler.set_data(self.df)
        self.datatype_handler.set_data(self.df)
        self.text_standardizer.set_data(self.df)

    # ==================================================
    # Analyze
    # ==================================================

    def analyze(self):
        """Analyze the current dataset."""

        if self.df is None:
            raise ValueError("Please load a dataset first.")

        self._sync_handlers()

        return self.analyzer.analyze()

    # ==================================================
    # Display Analysis
    # ==================================================

    def display_analysis(self):
        """Display a complete analysis report."""

        if self.df is None:
            raise ValueError("Please load a dataset first.")

        self._sync_handlers()
        self.analyzer.display_report()

    # ==================================================
    # Text Standardization
    # ==================================================

    def standardize_text(
        self,
        columns=None,
        case="lower",
        normalize_categories=True
    ):
        """
        Standardize text and categorical values.

        Operations:
        - Trim whitespace
        - Standardize case
        - Normalize category labels
        """

        if self.df is None:
            raise ValueError("Please load a dataset first.")

        self._sync_handlers()

        before = self.df.copy()

        self.text_standardizer.standardize(
            columns=columns,
            case=case,
            normalize_categories=normalize_categories
        )

        self.df = self.text_standardizer.df

        changed_columns = 0

        for column in self.df.columns:
            if column in before.columns:
                if not before[column].astype("string").equals(
                    self.df[column].astype("string")
                ):
                    changed_columns += 1

        self.logger.success(
            module="TEXT_STANDARDIZATION",
            operation="STANDARDIZE_TEXT",
            description=(
                "Text whitespace, case and category "
                "standardization completed."
            ),
            columns_affected=changed_columns
        )

        self._sync_handlers()

        return self.df

    # ==================================================
    # Handle Missing Values
    # ==================================================

    def handle_missing_values(
        self,
        numeric_strategy="median",
        categorical_strategy="mode",
        missing_threshold=40
    ):
        """
        Handle missing values.

        Columns with missing percentage greater than
        missing_threshold are removed.

        Remaining missing values are filled.
        """

        self._sync_handlers()

        before_missing = self.df.isnull().sum().sum()

        # Remove high-missing columns
        self.missing_handler.drop_high_missing_columns(
            missing_threshold=missing_threshold
        )

        self.df = self.missing_handler.df

        self._sync_handlers()

        # Fill remaining missing values
        self.missing_handler.fill_numeric(
            strategy=numeric_strategy
        )

        self.missing_handler.fill_categorical(
            strategy=categorical_strategy
        )

        self.df = self.missing_handler.df

        after_missing = self.df.isnull().sum().sum()

        handled = int(
            before_missing - after_missing
        )

        self.logger.success(
            module="MISSING_VALUES",
            operation="HANDLE_MISSING_VALUES",
            description=(
                f"Missing values handled successfully. "
                f"Columns with more than "
                f"{missing_threshold}% missing values "
                f"were removed."
            ),
            rows_affected=handled
        )

        self._sync_handlers()

        return self.df

    # ==================================================
    # Remove Duplicates
    # ==================================================

    def remove_duplicates(
        self,
        subset=None,
        keep="first"
    ):
        """Remove duplicate rows."""

        self._sync_handlers()

        before = len(self.df)

        self.duplicate_handler.remove_duplicates(
            subset=subset,
            keep=keep
        )

        self.df = self.duplicate_handler.df

        removed = before - len(self.df)

        self.logger.success(
            module="DUPLICATES",
            operation="REMOVE_DUPLICATES",
            description=(
                "Duplicate rows removed successfully."
            ),
            rows_affected=removed
        )

        self._sync_handlers()

        return self.df

    # ==================================================
    # Remove IQR Outliers
    # ==================================================

    def remove_iqr_outliers(
        self,
        columns=None,
        multiplier=1.5
    ):
        """Remove numerical outliers using IQR."""

        self._sync_handlers()

        before = len(self.df)

        self.outlier_handler.remove_iqr_outliers(
            columns=columns,
            multiplier=multiplier
        )

        self.df = self.outlier_handler.df

        removed = before - len(self.df)

        self.logger.success(
            module="OUTLIERS",
            operation="REMOVE_IQR_OUTLIERS",
            description=(
                "IQR-based outliers removed successfully."
            ),
            rows_affected=removed
        )

        self._sync_handlers()

        return self.df

    # ==================================================
    # Remove Z-Score Outliers
    # ==================================================

    def remove_zscore_outliers(
        self,
        columns=None,
        threshold=3
    ):
        """Remove numerical outliers using Z-score."""

        self._sync_handlers()

        before = len(self.df)

        self.outlier_handler.remove_zscore_outliers(
            columns=columns,
            threshold=threshold
        )

        self.df = self.outlier_handler.df

        removed = before - len(self.df)

        self.logger.success(
            module="OUTLIERS",
            operation="REMOVE_ZSCORE_OUTLIERS",
            description=(
                "Z-score outliers removed successfully."
            ),
            rows_affected=removed
        )

        self._sync_handlers()

        return self.df

    # ==================================================
    # Convert Data Types
    # ==================================================

    def auto_convert_datatypes(self):
        """Automatically detect and convert obvious data types."""

        self._sync_handlers()

        before_types = (
            self.df.dtypes.astype(str).to_dict()
        )

        self.datatype_handler.auto_convert()

        self.df = self.datatype_handler.df

        after_types = (
            self.df.dtypes.astype(str).to_dict()
        )

        changed_columns = sum(
            1
            for column in before_types
            if before_types[column]
            != after_types[column]
        )

        self.logger.success(
            module="DATATYPE",
            operation="AUTO_CONVERT",
            description=(
                "Automatic data type conversion completed."
            ),
            columns_affected=changed_columns
        )

        self._sync_handlers()

        return self.df

    # ==================================================
    # Complete Cleaning
    # ==================================================

    def clean(
        self,
        remove_duplicates=True,
        handle_missing=True,
        remove_outliers=False,
        convert_datatypes=True,
        outlier_method="iqr",
        missing_threshold=40,
        standardize_text=True,
        text_case="lower",
        normalize_categories=True
    ):
        """
        Run the complete DataMop cleaning pipeline.
        """

        if self.df is None:
            raise ValueError(
                "Please load a dataset first."
            )

        if not isinstance(
            missing_threshold,
            (int, float)
        ):
            raise TypeError(
                "missing_threshold must be a number "
                "between 0 and 100."
            )

        if not 0 <= missing_threshold <= 100:
            raise ValueError(
                "missing_threshold must be between "
                "0 and 100."
            )

        print("\n")
        print("=" * 70)
        print("              DATAMOP CLEANING PIPELINE")
        print("=" * 70)

        # ----------------------------------------------
        # 1. Data Types
        # ----------------------------------------------

        if convert_datatypes:

            print("\n[1/5] Converting data types...")

            self.auto_convert_datatypes()

        # ----------------------------------------------
        # 2. Text Standardization
        # ----------------------------------------------

        if standardize_text:

            print(
                "\n[2/5] Standardizing text values..."
            )

            self.standardize_text(
                case=text_case,
                normalize_categories=normalize_categories
            )

        # ----------------------------------------------
        # 3. Missing Values
        # ----------------------------------------------

        if handle_missing:

            print(
                f"\n[3/5] Handling missing values "
                f"(threshold: {missing_threshold}%)..."
            )

            self.handle_missing_values(
                missing_threshold=missing_threshold
            )

        # ----------------------------------------------
        # 4. Duplicates
        # ----------------------------------------------

        if remove_duplicates:

            print("\n[4/5] Removing duplicates...")

            self.remove_duplicates()

        # ----------------------------------------------
        # 5. Outliers
        # ----------------------------------------------

        if remove_outliers:

            print("\n[5/5] Handling outliers...")

            if outlier_method.lower() == "iqr":

                self.remove_iqr_outliers()

            elif outlier_method.lower() == "zscore":

                self.remove_zscore_outliers()

            else:

                raise ValueError(
                    "outlier_method must be "
                    "'iqr' or 'zscore'."
                )

        print("\n")
        print("=" * 70)
        print("              CLEANING COMPLETED")
        print("=" * 70)

        return self.df

    # ==================================================
    # Save
    # ==================================================

    def save(self, filepath):
        """Save the cleaned DataFrame to CSV or Excel."""

        if self.df is None:
            raise ValueError(
                "No dataset available to save."
            )

        if filepath.lower().endswith(".csv"):

            self.df.to_csv(
                filepath,
                index=False
            )

        elif filepath.lower().endswith(
            (".xlsx", ".xls")
        ):

            self.df.to_excel(
                filepath,
                index=False
            )

        else:

            raise ValueError(
                "Unsupported file format. "
                "Use CSV or Excel."
            )

        self.logger.success(
            module="SAVER",
            operation="SAVE_DATASET",
            description=(
                f"Cleaned dataset saved to {filepath}."
            ),
            rows_affected=len(self.df),
            columns_affected=len(self.df.columns)
        )

        print(
            f"\nDataset saved successfully: {filepath}"
        )

        return filepath

    # ==================================================
    # Cleaning Log
    # ==================================================

    def cleaning_log(self):
        """Display the complete DataMop cleaning log."""

        self.logger.display_logs()

    # ==================================================
    # Get Cleaning Log
    # ==================================================

    def get_cleaning_log(self):
        """Return the complete DataMop cleaning log as DataFrame."""

        return self.logger.to_dataframe()

    # ==================================================
    # Get DataFrame
    # ==================================================

    def get_dataframe(self):
        """Return the current DataFrame."""

        return self.df