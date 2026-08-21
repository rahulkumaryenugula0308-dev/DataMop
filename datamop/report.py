"""
DataMop - Automatic Data Quality Report

This module generates an HTML report containing:

- Dataset summary
- Data quality information
- Missing values
- Duplicate information
- Data type information
- Numerical statistics
- Cleaning history
- Generated visualizations
"""

import os
import html
from datetime import datetime

import pandas as pd
import numpy as np


class DataReport:
    """
    Generate an automatic DataMop HTML report.
    """

    def __init__(
        self,
        dataframe=None,
        cleaning_log=None,
        visualization_files=None
    ):
        """
        Initialize DataReport.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset to report.

        cleaning_log : pandas.DataFrame, list, optional
            Cleaning history.

        visualization_files : list, optional
            Generated visualization file paths.
        """

        self.df = dataframe

        self.cleaning_log = (
            cleaning_log
            if cleaning_log is not None
            else []
        )

        self.visualization_files = (
            visualization_files
            if visualization_files is not None
            else []
        )

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

        return self.df

    # ==================================================
    # Set Cleaning Log
    # ==================================================

    def set_cleaning_log(self, cleaning_log):
        """
        Set cleaning log.
        """

        self.cleaning_log = cleaning_log

        return self.cleaning_log

    # ==================================================
    # Set Visualizations
    # ==================================================

    def set_visualizations(
        self,
        visualization_files
    ):
        """
        Set visualization files.
        """

        self.visualization_files = (
            visualization_files
        )

        return self.visualization_files

    # ==================================================
    # Check Data
    # ==================================================

    def _check_data(self):
        """
        Check whether data is available.
        """

        if self.df is None:
            raise ValueError(
                "No dataset available for report generation."
            )

    # ==================================================
    # Dataset Summary
    # ==================================================

    def dataset_summary(self):
        """
        Return basic dataset information.
        """

        self._check_data()

        numerical_columns = (
            self.df.select_dtypes(
                include=np.number
            ).columns
        )

        categorical_columns = (
            self.df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "string",
                    "bool"
                ]
            ).columns
        )

        memory_usage = (
            self.df.memory_usage(
                deep=True
            ).sum()
        )

        memory_mb = (
            memory_usage / (
                1024 * 1024
            )
        )

        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "numerical_columns": len(
                numerical_columns
            ),
            "categorical_columns": len(
                categorical_columns
            ),
            "memory_mb": round(
                memory_mb,
                2
            )
        }

    # ==================================================
    # Missing Values
    # ==================================================

    def missing_value_summary(self):
        """
        Generate missing-value summary.
        """

        self._check_data()

        missing_count = (
            self.df.isnull()
            .sum()
        )

        missing_percentage = (
            self.df.isnull()
            .mean()
            * 100
        )

        report = pd.DataFrame({
            "column": self.df.columns,
            "missing_count":
                missing_count.values,
            "missing_percentage":
                missing_percentage.values
        })

        return report[
            report["missing_count"] > 0
        ].sort_values(
            by="missing_count",
            ascending=False
        ).reset_index(drop=True)

    # ==================================================
    # Duplicate Summary
    # ==================================================

    def duplicate_summary(self):
        """
        Generate duplicate summary.
        """

        self._check_data()

        duplicate_count = int(
            self.df.duplicated()
            .sum()
        )

        total_rows = len(self.df)

        percentage = (
            duplicate_count
            / total_rows
            * 100
            if total_rows > 0
            else 0
        )

        return {
            "duplicate_count":
                duplicate_count,
            "duplicate_percentage":
                round(
                    percentage,
                    2
                )
        }

    # ==================================================
    # Data Type Summary
    # ==================================================

    def datatype_summary(self):
        """
        Generate data type summary.
        """

        self._check_data()

        result = []

        for column in self.df.columns:

            result.append({
                "column": column,
                "data_type": str(
                    self.df[column].dtype
                ),
                "non_null": int(
                    self.df[column].notna()
                    .sum()
                ),
                "unique_values": int(
                    self.df[column].nunique(
                        dropna=False
                    )
                )
            })

        return pd.DataFrame(result)

    # ==================================================
    # Numerical Summary
    # ==================================================

    def numerical_summary(self):
        """
        Generate numerical statistics.
        """

        self._check_data()

        numerical_columns = (
            self.df.select_dtypes(
                include=np.number
            ).columns
        )

        if len(numerical_columns) == 0:
            return pd.DataFrame()

        statistics = (
            self.df[
                numerical_columns
            ]
            .describe()
            .T
            .reset_index()
        )

        statistics = statistics.rename(
            columns={
                "index": "column"
            }
        )

        return statistics

    # ==================================================
    # Cleaning Log DataFrame
    # ==================================================

    def _log_dataframe(self):
        """
        Convert cleaning log into DataFrame.
        """

        if self.cleaning_log is None:
            return pd.DataFrame()

        if isinstance(
            self.cleaning_log,
            pd.DataFrame
        ):
            return self.cleaning_log

        if isinstance(
            self.cleaning_log,
            list
        ):

            if not self.cleaning_log:
                return pd.DataFrame()

            return pd.DataFrame(
                self.cleaning_log
            )

        return pd.DataFrame()

    # ==================================================
    # HTML Escape
    # ==================================================

    def _safe_html(self, value):
        """
        Safely convert text to HTML.
        """

        return html.escape(
            str(value)
        )

    # ==================================================
    # Generate HTML Table
    # ==================================================

    def _dataframe_to_html(
        self,
        dataframe
    ):
        """
        Convert DataFrame into HTML table.
        """

        if dataframe is None:
            return "<p>No data available.</p>"

        if dataframe.empty:
            return "<p>No records available.</p>"

        return dataframe.to_html(
            index=False,
            classes="data-table",
            border=0
        )

    # ==================================================
    # Generate Visualization Section
    # ==================================================

    def _visualization_html(
        self,
        report_directory
    ):
        """
        Create HTML for visualization files.
        """

        if not self.visualization_files:

            return """
            <p>
                No visualization files were provided.
            </p>
            """

        content = ""

        for filepath in self.visualization_files:

            if not os.path.exists(filepath):
                continue

            filename = os.path.basename(
                filepath
            )

            relative_path = os.path.relpath(
                filepath,
                report_directory
            )

            relative_path = (
                relative_path
                .replace("\\", "/")
            )

            title = (
                os.path.splitext(
                    filename
                )[0]
                .replace("_", " ")
                .title()
            )

            content += f"""
            <div class="chart-card">
                <h3>
                    {self._safe_html(title)}
                </h3>

                <img
                    src="{self._safe_html(relative_path)}"
                    alt="{self._safe_html(title)}"
                >
            </div>
            """

        if not content:

            return """
            <p>
                No valid visualization files found.
            </p>
            """

        return content

    # ==================================================
    # Generate Report
    # ==================================================

    def generate(
        self,
        filepath="reports/datamop_report.html",
        title="DataMop Data Quality Report"
    ):
        """
        Generate complete HTML report.

        Parameters
        ----------
        filepath : str
            Output HTML file.

        title : str
            Report title.

        Returns
        -------
        str
            Generated report path.
        """

        self._check_data()

        report_directory = os.path.dirname(
            os.path.abspath(filepath)
        )

        os.makedirs(
            report_directory,
            exist_ok=True
        )

        summary = self.dataset_summary()

        missing = (
            self.missing_value_summary()
        )

        duplicates = (
            self.duplicate_summary()
        )

        datatypes = (
            self.datatype_summary()
        )

        numerical = (
            self.numerical_summary()
        )

        logs = (
            self._log_dataframe()
        )

        generated_time = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        dataset_name = (
            "DataFrame"
        )

        # ------------------------------------------------
        # Summary Cards
        # ------------------------------------------------

        summary_cards = f"""
        <div class="summary-grid">

            <div class="summary-card">
                <h3>Rows</h3>
                <p>{summary["rows"]:,}</p>
            </div>

            <div class="summary-card">
                <h3>Columns</h3>
                <p>{summary["columns"]:,}</p>
            </div>

            <div class="summary-card">
                <h3>Numerical</h3>
                <p>
                    {summary["numerical_columns"]:,}
                </p>
            </div>

            <div class="summary-card">
                <h3>Categorical</h3>
                <p>
                    {summary["categorical_columns"]:,}
                </p>
            </div>

            <div class="summary-card">
                <h3>Missing Cells</h3>
                <p>
                    {int(
                        self.df.isnull()
                        .sum()
                        .sum()
                    ):,}
                </p>
            </div>

            <div class="summary-card">
                <h3>Duplicates</h3>
                <p>
                    {duplicates["duplicate_count"]:,}
                </p>
            </div>

        </div>
        """

        # ------------------------------------------------
        # Missing Values Section
        # ------------------------------------------------

        missing_html = (
            self._dataframe_to_html(
                missing
            )
        )

        # ------------------------------------------------
        # Data Type Section
        # ------------------------------------------------

        datatype_html = (
            self._dataframe_to_html(
                datatypes
            )
        )

        # ------------------------------------------------
        # Numerical Section
        # ------------------------------------------------

        numerical_html = (
            self._dataframe_to_html(
                numerical
            )
        )

        # ------------------------------------------------
        # Cleaning Log Section
        # ------------------------------------------------

        logs_html = (
            self._dataframe_to_html(
                logs
            )
        )

        # ------------------------------------------------
        # Visualization Section
        # ------------------------------------------------

        visualization_html = (
            self._visualization_html(
                report_directory
            )
        )

        # ------------------------------------------------
        # Complete HTML
        # ------------------------------------------------

        html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>
    {self._safe_html(title)}
</title>

<style>

body {{
    font-family:
        Arial,
        Helvetica,
        sans-serif;

    margin: 0;

    padding: 0;

    background: #f5f7fa;

    color: #222;
}}

.header {{
    background: #1f2937;

    color: white;

    padding: 35px;

    text-align: center;
}}

.header h1 {{
    margin: 0 0 10px 0;
}}

.header p {{
    margin: 5px;
}}

.container {{
    width: 92%;

    max-width: 1400px;

    margin: 30px auto;
}}

.section {{
    background: white;

    padding: 25px;

    margin-bottom: 25px;

    border-radius: 10px;

    box-shadow:
        0 2px 8px
        rgba(0, 0, 0, 0.08);
}}

.section h2 {{
    margin-top: 0;

    border-bottom:
        2px solid #e5e7eb;

    padding-bottom: 10px;
}}

.summary-grid {{
    display: grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(180px, 1fr)
        );

    gap: 15px;

    margin-top: 20px;
}}

.summary-card {{
    background: #f8fafc;

    padding: 20px;

    border-radius: 8px;

    text-align: center;

    border:
        1px solid #e5e7eb;
}}

.summary-card h3 {{
    margin: 0 0 10px 0;

    font-size: 15px;

    color: #6b7280;
}}

.summary-card p {{
    margin: 0;

    font-size: 28px;

    font-weight: bold;
}}

.data-table {{
    width: 100%;

    border-collapse:
        collapse;

    margin-top: 15px;

    font-size: 14px;
}}

.data-table th,
.data-table td {{
    border:
        1px solid #ddd;

    padding: 10px;

    text-align: left;
}}

.data-table th {{
    background: #f3f4f6;

    font-weight: bold;
}}

.data-table tr:nth-child(even) {{
    background: #fafafa;
}}

.chart-card {{
    margin-bottom: 35px;

    padding: 20px;

    border:
        1px solid #e5e7eb;

    border-radius: 8px;

    text-align: center;
}}

.chart-card h3 {{
    margin-top: 0;
}}

.chart-card img {{
    max-width: 100%;

    height: auto;
}}

.footer {{
    text-align: center;

    padding: 25px;

    color: #6b7280;

    font-size: 13px;
}}

</style>

</head>

<body>

<div class="header">

    <h1>
        {self._safe_html(title)}
    </h1>

    <p>
        Generated by DataMop
    </p>

    <p>
        Generated on:
        {self._safe_html(generated_time)}
    </p>

</div>


<div class="container">


<!-- ========================================= -->
<!-- DATASET SUMMARY -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Dataset Summary
    </h2>

    <p>
        This section provides a high-level
        overview of the dataset.
    </p>

    {summary_cards}

</div>


<!-- ========================================= -->
<!-- DUPLICATE SUMMARY -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Duplicate Analysis
    </h2>

    <p>
        Duplicate rows:
        <strong>
            {duplicates["duplicate_count"]:,}
        </strong>
    </p>

    <p>
        Duplicate percentage:
        <strong>
            {duplicates["duplicate_percentage"]}%
        </strong>
    </p>

</div>


<!-- ========================================= -->
<!-- MISSING VALUES -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Missing Value Analysis
    </h2>

    {missing_html}

</div>


<!-- ========================================= -->
<!-- DATA TYPES -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Data Type Analysis
    </h2>

    {datatype_html}

</div>


<!-- ========================================= -->
<!-- NUMERICAL STATISTICS -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Numerical Statistics
    </h2>

    {numerical_html}

</div>


<!-- ========================================= -->
<!-- VISUALIZATIONS -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Data Visualizations
    </h2>

    <p>
        Automatically generated visualizations
        for the dataset.
    </p>

    {visualization_html}

</div>


<!-- ========================================= -->
<!-- CLEANING LOG -->
<!-- ========================================= -->

<div class="section">

    <h2>
        Cleaning History
    </h2>

    {logs_html}

</div>


</div>


<div class="footer">

    DataMop Automatic Data Quality Report

</div>


</body>

</html>
"""

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                html_content
            )

        return filepath