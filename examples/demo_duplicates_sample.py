import pandas as pd

from datamop.duplicates import DuplicateHandler


# Create sample dataset

data = {
    "Name": [
        "Rahul",
        "Sanjana",
        "Rahul",
        "Akshithaa",
        "Sanjana"
    ],

    "Age": [
        22,
        21,
        22,
        23,
        21
    ],

    "City": [
        "Hyderabad",
        "Chennai",
        "Hyderabad",
        "Bangalore",
        "Chennai"
    ]
}


df = pd.DataFrame(data)


print("========== ORIGINAL DATA ==========")
print(df)


# Create handler

handler = DuplicateHandler(df)


# Display report

handler.display_report()


# Display duplicates

handler.display_duplicates()


# Remove duplicates

handler.remove_duplicates()


print("\n========== AFTER CLEANING ==========")

print(handler.df)


# Display log

handler.display_log()
