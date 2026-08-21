from datamop.loader import DataLoader
from datamop.duplicates import DuplicateHandler


# ==================================================
# STEP 1 - Load Dataset
# ==================================================

loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset.csv"
)


# ==================================================
# STEP 2 - Create Duplicate Handler
# ==================================================

handler = DuplicateHandler(df)


# ==================================================
# STEP 3 - Display Duplicate Report
# ==================================================

handler.display_report()


# ==================================================
# STEP 4 - Display Duplicate Records
# ==================================================

handler.display_duplicates()


# ==================================================
# STEP 5 - Remove Duplicate Rows
# ==================================================

handler.remove_duplicates()


# ==================================================
# STEP 6 - Check Again
# ==================================================

print("\nAFTER DUPLICATE REMOVAL")

handler.display_report()


# ==================================================
# STEP 7 - Display Cleaning Log
# ==================================================

handler.display_log()