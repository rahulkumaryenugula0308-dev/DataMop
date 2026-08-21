"""
DataMop - Centralized Cleaning Logger

This module records all important operations performed
during the DataMop data processing pipeline.
"""

import os
from datetime import datetime

import pandas as pd


class DataLogger:
    """
    Centralized logger for DataMop operations.
    """

    def __init__(self):
        """
        Initialize the logger.
        """

        self.logs = []

    # ==================================================
    # Add Log
    # ==================================================

    def add_log(
        self,
        module,
        operation,
        description,
        rows_affected=0,
        columns_affected=0,
        status="SUCCESS"
    ):
        """
        Add an operation to the cleaning log.

        Parameters
        ----------
        module : str
            Name of the module performing the operation.

        operation : str
            Name of the operation.

        description : str
            Detailed description.

        rows_affected : int
            Number of affected rows.

        columns_affected : int
            Number of affected columns.

        status : str
            Operation status.
        """

        log_entry = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "module": str(module),
            "operation": str(operation),
            "description": str(description),
            "rows_affected": int(rows_affected),
            "columns_affected": int(columns_affected),
            "status": str(status)
        }

        self.logs.append(log_entry)

        return log_entry

    # ==================================================
    # Success Log
    # ==================================================

    def success(
        self,
        module,
        operation,
        description,
        rows_affected=0,
        columns_affected=0
    ):
        """
        Add a successful operation log.
        """

        return self.add_log(
            module=module,
            operation=operation,
            description=description,
            rows_affected=rows_affected,
            columns_affected=columns_affected,
            status="SUCCESS"
        )

    # ==================================================
    # Warning Log
    # ==================================================

    def warning(
        self,
        module,
        operation,
        description,
        rows_affected=0,
        columns_affected=0
    ):
        """
        Add a warning log.
        """

        return self.add_log(
            module=module,
            operation=operation,
            description=description,
            rows_affected=rows_affected,
            columns_affected=columns_affected,
            status="WARNING"
        )

    # ==================================================
    # Error Log
    # ==================================================

    def error(
        self,
        module,
        operation,
        description
    ):
        """
        Add an error log.
        """

        return self.add_log(
            module=module,
            operation=operation,
            description=description,
            status="ERROR"
        )

    # ==================================================
    # Get Logs
    # ==================================================

    def get_logs(self):
        """
        Return all logs as a list of dictionaries.
        """

        return self.logs.copy()

    # ==================================================
    # Get DataFrame
    # ==================================================

    def to_dataframe(self):
        """
        Convert logs into a pandas DataFrame.
        """

        if not self.logs:
            return pd.DataFrame(
                columns=[
                    "timestamp",
                    "module",
                    "operation",
                    "description",
                    "rows_affected",
                    "columns_affected",
                    "status"
                ]
            )

        return pd.DataFrame(self.logs)

    # ==================================================
    # Display Logs
    # ==================================================

    def display_logs(self):
        """
        Display all logs in a readable format.
        """

        print("\n")
        print("=" * 100)
        print("                         DATAMOP CLEANING LOG")
        print("=" * 100)

        if not self.logs:

            print("No operations have been logged.")

        else:

            for number, log in enumerate(
                self.logs,
                start=1
            ):

                print(f"\nOperation {number}")
                print("-" * 100)

                print(
                    f"Timestamp         : "
                    f"{log['timestamp']}"
                )

                print(
                    f"Module            : "
                    f"{log['module']}"
                )

                print(
                    f"Operation         : "
                    f"{log['operation']}"
                )

                print(
                    f"Description       : "
                    f"{log['description']}"
                )

                print(
                    f"Rows Affected     : "
                    f"{log['rows_affected']}"
                )

                print(
                    f"Columns Affected  : "
                    f"{log['columns_affected']}"
                )

                print(
                    f"Status            : "
                    f"{log['status']}"
                )

        print("\n" + "=" * 100)

    # ==================================================
    # Filter by Module
    # ==================================================

    def get_logs_by_module(self, module):
        """
        Return logs belonging to a specific module.
        """

        return [
            log
            for log in self.logs
            if log["module"].lower()
            == module.lower()
        ]

    # ==================================================
    # Filter by Status
    # ==================================================

    def get_logs_by_status(self, status):
        """
        Return logs with a specific status.
        """

        return [
            log
            for log in self.logs
            if log["status"].lower()
            == status.lower()
        ]

    # ==================================================
    # Count Operations
    # ==================================================

    def count(self):
        """
        Return total number of logged operations.
        """

        return len(self.logs)

    # ==================================================
    # Clear Logs
    # ==================================================

    def clear(self):
        """
        Clear all logs.
        """

        self.logs.clear()

    # ==================================================
    # Save Logs to CSV
    # ==================================================

    def save_csv(self, filepath):
        """
        Save logs to a CSV file.

        Parameters
        ----------
        filepath : str
            Output CSV path.
        """

        directory = os.path.dirname(filepath)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        df = self.to_dataframe()

        df.to_csv(
            filepath,
            index=False
        )

        return filepath

    # ==================================================
    # Save Logs to Excel
    # ==================================================

    def save_excel(self, filepath):
        """
        Save logs to an Excel file.

        Parameters
        ----------
        filepath : str
            Output Excel path.
        """

        directory = os.path.dirname(filepath)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        df = self.to_dataframe()

        df.to_excel(
            filepath,
            index=False
        )

        return filepath