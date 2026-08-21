import datamop


print("=" * 70)
print("              DATAMOP FULL PIPELINE")
print("=" * 70)


result = datamop.auto_clean(
    "datasets/Titanic-Dataset.csv",
    output_dir="datamop_output"
)


print("\n" + "=" * 70)
print("                    RESULT")
print("=" * 70)


print("\nCleaned Dataset:")
print(result["cleaned_file"])


print("\nReport:")
print(result["report"])


print("\nCleaning Log:")
print(result["cleaning_log"])


print("\nVisualizations:")

for chart in result["visualizations"]:

    print(chart)


print("\n" + "=" * 70)
print("              PIPELINE COMPLETED")
print("=" * 70)