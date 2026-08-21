from datamop.loader import DataLoader
from datamop.missing_values import MissingValueHandler


loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset-selected-columns.csv"
)

handler = MissingValueHandler(df)

print("BEFORE:")
print(handler.df.shape)

handler.drop_columns(
    missing_threshold=50
)

print("\nAFTER:")
print(handler.df.shape)

handler.display_log()