from datamop.loader import load_file
from datamop.text import clean_text

file_path = r"C:\Users\Ajay\Downloads\train.csv"

df = load_file(file_path)

cleaned_df = clean_text(
    df,
    operation="normalize"
)

print("=" * 50)
print("ORIGINAL DATA")
print("=" * 50)

print(df[["Name", "Sex", "Embarked"]].head())

print("\n" + "=" * 50)
print("CLEANED DATA")
print("=" * 50)

print(cleaned_df[["Name", "Sex", "Embarked"]].head())