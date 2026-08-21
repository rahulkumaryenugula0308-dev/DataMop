from datamop.loader import DataLoader
from datamop.profiler import ColumnProfiler


loader = DataLoader()

df = loader.load(
    "datasets/Titanic-Dataset.csv"
)


profiler = ColumnProfiler(df)


profiler.display_profile()


print("\nCOLUMN GROUPS")

print(
    "\nIDs:"
)

print(
    profiler.get_columns_by_type(
        "id"
    )
)


print(
    "\nContinuous:"
)

print(
    profiler.get_columns_by_type(
        "numeric_continuous"
    )
)


print(
    "\nDiscrete:"
)

print(
    profiler.get_columns_by_type(
        "numeric_discrete"
    )
)


print(
    "\nCategorical:"
)

print(
    profiler.get_columns_by_type(
        "categorical"
    )
)


print(
    "\nBinary:"
)

print(
    profiler.get_columns_by_type(
        "binary"
    )
)