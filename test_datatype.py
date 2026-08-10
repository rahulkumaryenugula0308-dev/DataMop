import pandas as pd
import pytest

from datamop.datatype import (
    detect_type,
    convert_numeric,
    convert_datetime,
    convert_boolean,
    datatype_summary
)


def sample_dataframe():
    return pd.DataFrame({
        "Marks": [
            "90",
            "80",
            "invalid"
        ],
        "Date": [
            "2025-01-01",
            "2025-02-01",
            "invalid"
        ],
        "Passed": [
            "Yes",
            "No",
            "True"
        ]
    })


def test_detect_type():
    df = sample_dataframe()

    result = detect_type(df)

    assert isinstance(result, pd.Series)
    assert len(result) == 3


def test_convert_numeric():
    df = sample_dataframe()

    result = convert_numeric(df, "Marks")

    assert pd.api.types.is_numeric_dtype(
        result["Marks"]
    )

    assert pd.isna(result.loc[2, "Marks"])


def test_convert_datetime():
    df = sample_dataframe()

    result = convert_datetime(df, "Date")

    assert pd.api.types.is_datetime64_any_dtype(
        result["Date"]
    )


def test_convert_boolean():
    df = sample_dataframe()

    result = convert_boolean(df, "Passed")

    assert str(result["Passed"].dtype) == "boolean"

    assert result.loc[0, "Passed"] is True
    assert result.loc[1, "Passed"] is False


def test_datatype_summary():
    df = sample_dataframe()

    result = datatype_summary(df)

    assert "Marks" in result
    assert "Date" in result
    assert "Passed" in result

    assert "datatype" in result["Marks"]
    assert "missing_values" in result["Marks"]


def test_invalid_dataframe():
    with pytest.raises(TypeError):
        detect_type("not a dataframe")


def test_invalid_column():
    df = sample_dataframe()

    with pytest.raises(ValueError):
        convert_numeric(df, "WrongColumn")