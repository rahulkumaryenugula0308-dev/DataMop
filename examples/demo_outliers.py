from datamop.loader import DataLoader
from datamop.outliers import OutlierHandler


# ==================================================
# Load Dataset
# ==================================================

loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset.csv"
)


# ==================================================
# Create Outlier Handler
# ==================================================

handler = OutlierHandler(df)


# ==================================================
# Show Numerical Columns
# ==================================================

print("\nNumerical Columns:")

print(
    handler.get_numerical_columns()
)


# ==================================================
# IQR Analysis
# ==================================================

handler.display_iqr_report()


# ==================================================
# Z-Score Analysis
# ==================================================

handler.display_zscore_report()


# ==================================================
# Display Log
# ==================================================

handler.display_log()