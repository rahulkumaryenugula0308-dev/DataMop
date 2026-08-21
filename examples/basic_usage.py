import datamop


result = datamop.auto_clean(
    "datasets/Titanic-Dataset.csv"
)


print("\n========== DATAMOP RESULT ==========")

print("Cleaned File:")
print(result["cleaned_file"])

print("\nReport:")
print(result["report"])

print("\nCleaning Log:")
print(result["cleaning_log"])

print("\nCharts Generated:")
print(len(result["visualizations"]))