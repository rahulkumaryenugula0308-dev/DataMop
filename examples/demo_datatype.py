from datamop.loader import DataLoader
from datamop.datatype import DataTypeHandler


# ==================================================
# STEP 1 - Load Dataset
# ==================================================

loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset.csv"
)


# ==================================================
# STEP 2 - Create Data Type Handler
# ==================================================

handler = DataTypeHandler(df)


# ==================================================
# STEP 3 - Display Current Types
# ==================================================

handler.display_report()


# ==================================================
# STEP 4 - Detect Numeric Candidates
# ==================================================

print("\nNUMERIC CANDIDATES")
print("-" * 80)

print(
    handler.detect_numeric_candidates()
)


# ==================================================
# STEP 5 - Detect Datetime Candidates
# ==================================================

print("\nDATETIME CANDIDATES")
print("-" * 80)

print(
    handler.detect_datetime_candidates()
)


# ==================================================
# STEP 6 - Automatic Conversion
# ==================================================

handler.auto_convert()


# ==================================================
# STEP 7 - Display Types After Conversion
# ==================================================

print("\nAFTER AUTOMATIC CONVERSION")

handler.display_report()


# ==================================================
# STEP 8 - Display Log
# ==================================================

handler.display_log()