"""
test_datatype.py

Testing datatype.py

"""
import pandas as pd
from datamop.datatype import (
    detect_type,
    convert_numeric,
    convert_datetime,
    convert_boolean,
    datatype_summary
)


# Sample DataFrame
data = {
    "Age": ["20", "25", "Thirty", "40"],
    "DOB": ["2004-05-12", "15/08/2001", "invalid", "2023-01-01"],
    "Passed": ["Yes", "No", "Y", "0"],
    "Name": ["Ram", "Sita", "John", "David"]
}

df = pd.DataFrame(data)

print("=" * 50)
print("Original DataFrame")
print(df)

print("\n" + "=" * 50)
print("Original Data Types")
print(detect_type(df))

print("\n" + "=" * 50)
print("Convert Age to Numeric")
convert_numeric(df, "Age")
print(df)
print(df.dtypes)

print("\n" + "=" * 50)
print("Convert DOB to Datetime")
convert_datetime(df, "DOB")
print(df)
print(df.dtypes)

print("\n" + "=" * 50)
print("Convert Passed to Boolean")
convert_boolean(df, "Passed")
print(df)
print(df.dtypes)

print("\n" + "=" * 50)
print("Datatype Summary")
print(datatype_summary(df))