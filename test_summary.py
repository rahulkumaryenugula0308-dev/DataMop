from datamop.loader import load_file
from datamop.summary import summary


file_path = r"C:\Users\Ajay\Downloads\train.csv"

df = load_file(file_path)

result = summary(df)

print("=" * 50)
print("DATASET SUMMARY")
print("=" * 50)

print(result["dataset"])

print("\n" + "=" * 50)
print("NUMERIC SUMMARY")
print("=" * 50)

print(result["numeric"])

print("\n" + "=" * 50)
print("CATEGORICAL SUMMARY")
print("=" * 50)

print(result["categorical"])