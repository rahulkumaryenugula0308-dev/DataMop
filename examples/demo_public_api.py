import pandas as pd
import datamop

result = datamop.analyze(
    "datasets/Titanic-Dataset.csv"
)

print("\n========== ANALYZE ==========")

print(
    result["analysis"]
)

result = datamop.clean(
    "datasets/Titanic-Dataset.csv"
)

print("\n========== CLEAN ==========")

print(
    result["dataframe"].head()
)

print(
    "\nCleaning Log:"
)

print(
    result["cleaning_log"]
)

result = datamop.visualize(
    "datasets/Titanic-Dataset.csv",
    output_dir="test_visual_output"
)

print("\n========== VISUALIZE ==========")

for chart in result["visualizations"]:
    print(chart)
    

df = pd.read_csv(
    "datasets/Titanic-Dataset.csv"
)


result = datamop.auto_clean(
    df,
    output_dir="dataframe_test"
)


print(
    "\n========== DATAFRAME TEST =========="
)

print(
    result["cleaned_dataframe"].head()
)

print(
    "\nCleaned file:"
)

print(
    result["cleaned_file"]
)