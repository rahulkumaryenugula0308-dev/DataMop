from datamop.loader import load_csv
from datamop.text import (
    trim_spaces,
    lower_case,
    upper_case,
    title_case,
    normalize_categories
)

# Load dataset
df = load_csv(r"C:\Users\Ajay\Downloads\train.csv")

print("=" * 50)
print("ORIGINAL DATA")
print("=" * 50)
print(df[["Name", "Sex", "Embarked"]].head())

print("\n" + "=" * 50)
print("TRIM SPACES")
print("=" * 50)
print(trim_spaces(df)[["Name", "Sex", "Embarked"]].head())

print("\n" + "=" * 50)
print("LOWER CASE")
print("=" * 50)
print(lower_case(df)[["Name", "Sex", "Embarked"]].head())

print("\n" + "=" * 50)
print("UPPER CASE")
print("=" * 50)
print(upper_case(df)[["Name", "Sex", "Embarked"]].head())

print("\n" + "=" * 50)
print("TITLE CASE")
print("=" * 50)
print(title_case(df)[["Name", "Sex", "Embarked"]].head())

print("\n" + "=" * 50)
print("NORMALIZED DATA")
print("=" * 50)
print(normalize_categories(df)[["Name", "Sex", "Embarked"]].head())