from datamop.logger import DataLogger


# ==================================================
# Create Logger
# ==================================================

logger = DataLogger()


# ==================================================
# Add Successful Operations
# ==================================================

logger.success(
    module="LOADER",
    operation="LOAD_DATASET",
    description="Titanic dataset loaded successfully.",
    rows_affected=891,
    columns_affected=12
)


logger.success(
    module="MISSING_VALUES",
    operation="FILL_MISSING_VALUES",
    description="Filled missing numerical values using median.",
    rows_affected=177,
    columns_affected=1
)


logger.success(
    module="DUPLICATES",
    operation="REMOVE_DUPLICATES",
    description="Removed duplicate records.",
    rows_affected=5,
    columns_affected=0
)


logger.success(
    module="OUTLIERS",
    operation="REMOVE_IQR_OUTLIERS",
    description="Removed IQR-based numerical outliers.",
    rows_affected=8,
    columns_affected=2
)


logger.success(
    module="DATATYPE",
    operation="CONVERT_DATATYPE",
    description="Converted Age column from object to numeric.",
    rows_affected=891,
    columns_affected=1
)


# ==================================================
# Display Logs
# ==================================================

logger.display_logs()


# ==================================================
# Display Count
# ==================================================

print("\nTotal Operations:")
print(logger.count())


# ==================================================
# Convert to DataFrame
# ==================================================

print("\nLog DataFrame:")

print(
    logger.to_dataframe()
)


# ==================================================
# Save Log
# ==================================================

logger.save_csv(
    "docs/cleaning_log.csv"
)

print(
    "\nLog saved successfully."
)