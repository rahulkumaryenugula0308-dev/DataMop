"""
DataMop - Automatic Data Processing Pipeline

High-level engine used by the public DataMop API.
"""

import os

import pandas as pd

from datamop.cleaner import DataCleaner
from datamop.analyzer import DataAnalyzer
from datamop.missing_values import MissingValueHandler
from datamop.duplicates import DuplicateHandler
from datamop.outliers import OutlierHandler
from datamop.datatype import DataTypeHandler
from datamop.text_standardization import TextStandardizer
from datamop.visualization import DataVisualizer
from datamop.report import DataReport
from datamop.validation import DataValidator


class DataMopPipeline:
    """
    Complete automatic DataMop pipeline.

    Supports:
        CSV files
        Excel files
        Pandas DataFrames
    """

    def __init__(
        self,
        output_dir="datamop_output"
    ):

        self.output_dir = output_dir

        self.cleaned_dir = os.path.join(
            output_dir,
            "cleaned_data"
        )

        self.visualization_dir = os.path.join(
            output_dir,
            "visualizations"
        )

        self.report_dir = os.path.join(
            output_dir,
            "reports"
        )

        os.makedirs(
            self.cleaned_dir,
            exist_ok=True
        )

        os.makedirs(
            self.visualization_dir,
            exist_ok=True
        )

        os.makedirs(
            self.report_dir,
            exist_ok=True
        )

        self.cleaner = DataCleaner()

        self.result = None

    # ==================================================
    # Validate Input
    # ==================================================

    def _validate_input(self, data):
        """
        Validate input using DataMopValidator.
        """

        return DataValidator.validate_input(
            data
        )

    # ==================================================
    # Load Input
    # ==================================================

    def _load_input(self, data):
        """
        Load either a file or a Pandas DataFrame.

        Supported inputs:
        - CSV
        - XLSX
        - XLS
        - pandas.DataFrame
        """

        input_type = self._validate_input(data)

        # ==================================================
        # FILE INPUT
        # ==================================================

        if input_type == "file":

            self.cleaner.load(data)

            filename = os.path.basename(data)

            name, extension = os.path.splitext(
                filename
            )

            return name

        # ==================================================
        # DATAFRAME INPUT
        # ==================================================

        if input_type == "dataframe":

            # Make a copy so DataMop never modifies
            # the user's original DataFrame directly.
            self.cleaner.df = data.copy()

            self.cleaner.filepath = None

            # ----------------------------------------------
            # Re-create internal handlers
            # ----------------------------------------------

            self.cleaner.analyzer = DataAnalyzer(
                self.cleaner.df
            )

            self.cleaner.missing_handler = (
                MissingValueHandler(
                    self.cleaner.df
                )
            )

            self.cleaner.duplicate_handler = (
                DuplicateHandler(
                    self.cleaner.df
                )
            )

            self.cleaner.outlier_handler = (
                OutlierHandler(
                    self.cleaner.df
                )
            )

            self.cleaner.datatype_handler = (
                DataTypeHandler(
                    self.cleaner.df
                )
            )

            # ----------------------------------------------
            # Text Standardization Handler
            # ----------------------------------------------

            self.cleaner.text_standardizer = (
                TextStandardizer(
                    self.cleaner.df
                )
            )

            return "dataframe"

        # ==================================================
        # FALLBACK DATAFRAME
        # ==================================================

        self.cleaner.df = data.copy()

        self.cleaner.filepath = None

        self.cleaner.analyzer = DataAnalyzer(
            self.cleaner.df
        )

        self.cleaner.missing_handler = (
            MissingValueHandler(
                self.cleaner.df
            )
        )

        self.cleaner.duplicate_handler = (
            DuplicateHandler(
                self.cleaner.df
            )
        )

        self.cleaner.outlier_handler = (
            OutlierHandler(
                self.cleaner.df
            )
        )

        self.cleaner.datatype_handler = (
            DataTypeHandler(
                self.cleaner.df
            )
        )

        self.cleaner.text_standardizer = (
            TextStandardizer(
                self.cleaner.df
            )
        )

        return "dataframe"

    # ==================================================
    # Run Full Pipeline
    # ==================================================

    def run(
        self,
        data,
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

        print("\n")
        print("=" * 70)
        print("                    DATAMOP")
        print("          AUTOMATIC DATA SCIENCE ENGINE")
        print("=" * 70)

        # ----------------------------------------------
        # 1. Load
        # ----------------------------------------------

        print("\n[1/5] Loading dataset...")

        dataset_name = (
            self._load_input(data)
        )

        # ----------------------------------------------
        # 2. Analyze
        # ----------------------------------------------

        print(
            "\n[2/5] Analyzing dataset..."
        )

        before_analysis = (
            self.cleaner.analyze()
        )

        # ----------------------------------------------
        # 3. Clean
        # ----------------------------------------------

        print(
            "\n[3/5] Cleaning dataset..."
        )

        self.cleaner.clean(
            remove_duplicates=(
                remove_duplicates
            ),
            handle_missing=(
                handle_missing
            ),
            remove_outliers=(
                remove_outliers
            ),
            convert_datatypes=(
                convert_datatypes
            ),
            outlier_method=(
                outlier_method
            ),
            missing_threshold=(
                missing_threshold
            ),
            standardize_text=(
                standardize_text
            ),
            text_case=(
                text_case
            ),
            normalize_categories=(
                normalize_categories
            )
        )

        cleaned_df = (
            self.cleaner.get_dataframe()
        )

        # ----------------------------------------------
        # 4. Visualization
        # ----------------------------------------------

        print(
            "\n[4/5] Generating visualizations..."
        )

        visualization_dir = os.path.join(
            self.visualization_dir,
            dataset_name
        )

        visualizer = DataVisualizer(
            cleaned_df,
            output_dir=visualization_dir
        )

        visualization_files = (
            visualizer.generate_all()
        )

        # ----------------------------------------------
        # 5. Save
        # ----------------------------------------------

        if dataset_name == "dataframe":

            cleaned_filename = (
                "dataframe_cleaned.csv"
            )

        else:

            cleaned_filename = (
                f"{dataset_name}_cleaned.csv"
            )

        cleaned_filepath = os.path.join(
            self.cleaned_dir,
            cleaned_filename
        )

        self.cleaner.save(
            cleaned_filepath
        )

        # ----------------------------------------------
        # Cleaning Log
        # ----------------------------------------------

        log_filepath = os.path.join(
            self.output_dir,
            "cleaning_log.csv"
        )

        self.cleaner.logger.save_csv(
            log_filepath
        )

        # ----------------------------------------------
        # Report
        # ----------------------------------------------

        print(
            "\n[5/5] Generating report..."
        )

        report_filepath = os.path.join(
            self.report_dir,
            f"{dataset_name}_report.html"
        )

        cleaning_log = (
            self.cleaner.get_cleaning_log()
        )

        report = DataReport(
            dataframe=cleaned_df,
            cleaning_log=cleaning_log,
            visualization_files=(
                visualization_files
            )
        )

        report.generate(
            report_filepath
        )

        # ----------------------------------------------
        # Result
        # ----------------------------------------------

        self.result = {

            "input": data,

            "cleaned_dataframe":
                cleaned_df,

            "cleaned_file":
                cleaned_filepath,

            "report":
                report_filepath,

            "cleaning_log":
                log_filepath,

            "visualizations":
                visualization_files,

            "analysis":
                before_analysis
        }

        print("\n")
        print("=" * 70)
        print(
            "             DATAMOP PROCESSING COMPLETED"
        )
        print("=" * 70)

        print(
            f"\nCleaned Dataset : "
            f"{cleaned_filepath}"
        )

        print(
            f"Report          : "
            f"{report_filepath}"
        )

        print(
            f"Cleaning Log    : "
            f"{log_filepath}"
        )

        print(
            f"Charts Generated: "
            f"{len(visualization_files)}"
        )

        print("\n" + "=" * 70)

        return self.result

    # ==================================================
    # Get Result
    # ==================================================

    def get_result(self):

        return self.result