import datamop


result = datamop.visualize(
    "datasets/Titanic-Dataset.csv"
)


print("\n========== VISUALIZATION RESULT ==========")

print(result)

print("\nCharts generated:")

if isinstance(result, list):

    for chart in result:
        print(chart)

else:

    print(result)