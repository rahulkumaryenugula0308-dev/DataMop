import pandas as pd
import pytest

from datamop.duplicates import (
    find_duplicates,
    drop_duplicates,
    find_near_duplicates,
    duplicate_summary
)


def sample_dataframe():
    return pd.DataFrame({
        "Name": [
            "Alice",
            "Bob",
            "Alice",
            "Charlie",
            "Bob"
        ],
        "Age": [
            25,
            30,
            25,
            40,
            30
        ]
    })


def test_find_duplicates():
    df = sample_dataframe()

    result = find_duplicates(df)

    assert len(result) == 2


def test_drop_duplicates():
    df = sample_dataframe()

    result = drop_duplicates(df)

    assert len(result) == 3
    assert result.index.tolist() == [0, 1, 2]


def test_duplicate_summary():
    df = sample_dataframe()

    result = duplicate_summary(df)

    assert result["total_rows"] == 5
    assert result["duplicate_rows"] == 2
    assert result["unique_rows"] == 3


def test_find_near_duplicates():
    df = pd.DataFrame({
        "Name": [
            "John Smith",
            "john smith",
            "Alice"
        ]
    })

    result = find_near_duplicates(
        df,
        threshold=0.90
    )

    assert len(result) >= 1


def test_invalid_dataframe():
    with pytest.raises(TypeError):
        find_duplicates("not a dataframe")


def test_invalid_threshold():
    df = sample_dataframe()

    with pytest.raises(ValueError):
        find_near_duplicates(df, threshold=2)
        