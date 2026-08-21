from datamop.loader import DataLoader


loader = DataLoader()

df = loader.load("datasets/Titanic-Dataset-selected-columns.csv")

print("\nFirst 5 rows:")
print(df.head())