import pandas as pd

from datamop.datatype import DataTypeHandler


data = {
    "Name": [
        "Rahul",
        "Sanjana",
        "Akshithaa",
        "Shurthy"
    ],

    "Age": [
        "21",
        "22",
        "23",
        "24"
    ],

    "Salary": [
        "30000",
        "35000",
        "40000",
        "45000"
    ],

    "JoiningDate": [
        "2026-01-10",
        "2026-02-15",
        "2026-03-20",
        "2026-04-25"
    ],

    "Active": [
        "Yes",
        "No",
        "Yes",
        "No"
    ]
}


df = pd.DataFrame(data)


print("========== ORIGINAL DATA TYPES ==========")

print(df.dtypes)


handler = DataTypeHandler(df)


print("\n========== TYPE REPORT ==========")

handler.display_report()


# Convert Age and Salary

handler.convert_to_numeric(
    ["Age", "Salary"]
)


# Convert JoiningDate

handler.convert_to_datetime(
    ["JoiningDate"]
)


# Convert Active

handler.convert_to_boolean(
    ["Active"]
)


print("\n========== AFTER CONVERSION ==========")

print(handler.df)

print("\n========== DATA TYPES ==========")

print(handler.df.dtypes)


print("\n========== LOG ==========")

handler.display_log()