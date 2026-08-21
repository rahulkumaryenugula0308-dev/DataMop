import pandas as pd
import datamop


df = pd.read_csv(
    "datasets/Titanic-Dataset.csv"
)


print("Original Dataset:")
print(df.head())


result = datamop.auto_clean(
    df
)


print("\n========== DATAMOP RESULT ==========")

print(result)