from datamop.loader import load_file
from datamop.missing import (
    detect_missing,
    clean_missing_values
)


file_path = r"C:\Users\Ajay\Downloads\train.csv"


# Load dataset
df = load_file(file_path)


print("=" * 50)
print("ORIGINAL DATASET")
print("=" * 50)

print("Shape:", df.shape)

print("\nMissing Values:")
print(detect_missing(df))


# Clean dataset
cleaned_df = clean_missing_values(
    df,
    threshold=40,
    numeric_method="mean",
    categorical_method="mode"
)


print("\n" + "=" * 50)
print("CLEANED DATASET")
print("=" * 50)

print("Shape:", cleaned_df.shape)

print("\nMissing Values:")
print(detect_missing(cleaned_df))
