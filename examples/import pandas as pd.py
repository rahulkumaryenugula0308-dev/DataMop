import pandas as pd
import datamop

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [30000, 40000, 50000]
})

result = datamop.auto_clean(df)

print(result)