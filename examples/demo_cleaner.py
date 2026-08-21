from datamop.cleaner import DataCleaner


# ==================================================
# STEP 1 - Create DataCleaner
# ==================================================

cleaner = DataCleaner()


# ==================================================
# STEP 2 - Load Dataset
# ==================================================

cleaner.load(
    "datasets/Titanic-Dataset.csv"
)


# ==================================================
# STEP 3 - Analyze BEFORE Cleaning
# ==================================================

print("\n========== BEFORE CLEANING ==========")

cleaner.display_analysis()


# ==================================================
# STEP 4 - Run Cleaning Pipeline
# ==================================================

cleaner.clean(
    remove_duplicates=True,
    handle_missing=True,
    remove_outliers=False,
    convert_datatypes=True
)


# ==================================================
# STEP 5 - Analyze AFTER Cleaning
# ==================================================

print("\n========== AFTER CLEANING ==========")

cleaner.display_analysis()


# ==================================================
# STEP 6 - Save Clean Dataset
# ==================================================

cleaner.save(
    "datasets/Titanic-Dataset_Cleaned.csv"
)


# ==================================================
# STEP 7 - Display Cleaning Log
# ==================================================

cleaner.cleaning_log()