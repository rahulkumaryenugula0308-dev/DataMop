import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe():
    """
    Small DataFrame used throughout DataMop tests.
    """

    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5],
        "Name": [
            "Alice",
            "Bob",
            "Charlie",
            "David",
            "Eva"
        ],
        "Age": [
            25,
            30,
            None,
            40,
            35
        ],
        "Salary": [
            30000,
            40000,
            35000,
            50000,
            45000
        ],
        "Gender": [
            "F",
            "M",
            "M",
            "M",
            "F"
        ],
        "Department": [
            "IT",
            "HR",
            "IT",
            "Finance",
            "HR"
        ]
    })


@pytest.fixture
def duplicate_dataframe():
    """
    DataFrame containing duplicate rows.
    """

    return pd.DataFrame({
        "Name": [
            "Alice",
            "Bob",
            "Alice",
            "Charlie"
        ],

        "Age": [
            25,
            30,
            25,
            35
        ]
    })


@pytest.fixture
def dataframe_with_missing_values():
    """
    DataFrame containing missing values.
    """

    return pd.DataFrame({
        "Name": [
            "Alice",
            "Bob",
            None,
            "David"
        ],

        "Age": [
            25,
            None,
            35,
            40
        ],

        "Salary": [
            30000,
            40000,
            None,
            50000
        ]
    })