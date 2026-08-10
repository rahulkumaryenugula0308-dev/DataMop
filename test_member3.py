import pandas as pd

from datamop.duplicates import (
    find_duplicates,
    drop_duplicates,
    find_near_duplicates,
    duplicate_summary
)

from datamop.datatype import (
    detect_type,
    convert_numeric,
    convert_datetime,
    convert_boolean,
    datatype_summary
)


df = pd.DataFrame({
    "Name": [
        "Alice",
        "Bob",
        "Alice",
        "Charlie"
    ],
    "Age": [
        "25",
        "30",
        "25",
        "40"
    ],
    "Date": [
        "2025-01-01",
        "2025-02-01",
        "2025-01-01",
        "invalid"
    ],
    "Passed": [
        "Yes",
        "No",
        "Yes",
        "True"
    ]
})


print("=" * 50)
print("ORIGINAL DATA")
print("=" * 50)
print(df)


print("\nDUPLICATES")
print(find_duplicates(df))


print("\nDUPLICATE SUMMARY")
print(duplicate_summary(df))


print("\nNEAR DUPLICATES")
print(find_near_duplicates(df))


cleaned = drop_duplicates(df)

print("\nAFTER REMOVING DUPLICATES")
print(cleaned)


cleaned = convert_numeric(cleaned, "Age")

cleaned = convert_datetime(cleaned, "Date")

cleaned = convert_boolean(cleaned, "Passed")


print("\nCONVERTED DATA")
print(cleaned)


print("\nDATA TYPES")
print(detect_type(cleaned))


print("\nDATATYPE SUMMARY")
print(datatype_summary(cleaned))
