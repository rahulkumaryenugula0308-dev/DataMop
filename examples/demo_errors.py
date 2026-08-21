import datamop
from datamop.exceptions import (
    DataMopError,
    DataMopInputError,
    DataMopFileError,
    DataMopDataError,
    DataMopConfigurationError
)

print("\n========== TEST 1 ==========")

try:

    datamop.auto_clean(
        "datasets/does_not_exist.csv"
    )

except Exception as error:

    print(
        type(error).__name__
    )

    print(
        error
    )


print("\n========== TEST 2 ==========")

try:

    datamop.auto_clean(
        "datasets/test.txt"
    )

except Exception as error:

    print(
        type(error).__name__
    )

    print(
        error
    )


print("\n========== TEST 3 ==========")

try:

    datamop.auto_clean(
        12345
    )

except Exception as error:

    print(
        type(error).__name__
    )

    print(
        error
    )
    
    
import pandas as pd
import datamop


print("\n========== TEST 4 ==========")

empty_df = pd.DataFrame()

try:

    datamop.auto_clean(
        empty_df
    )

except Exception as error:

    print(
        type(error).__name__
    )

    print(
        error
    )
    
print("\n========== TEST 5 ==========")

try:

    datamop.auto_clean(
        "datasets/Titanic-Dataset.csv",
        remove_outliers=True,
        outlier_method="wrong_method"
    )

except Exception as error:

    print(
        type(error).__name__
    )

    print(
        error
    )