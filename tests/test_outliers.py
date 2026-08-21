import pandas as pd

from datamop.outliers import OutlierHandler


def test_iqr_outlier_detection():

    df = pd.DataFrame({
        "Age": [
            20,
            21,
            22,
            23,
            24,
            1000
        ]
    })

    handler = OutlierHandler(df)

    result = handler.detect_iqr(
        "Age"
    )

    assert result is not None

    assert result["column"] == "Age"

    assert "q1" in result

    assert "q3" in result

    assert "iqr" in result

    assert "lower_bound" in result

    assert "upper_bound" in result

    assert "outlier_count" in result

    assert result["outlier_count"] > 0


def test_zscore_outlier_detection():

    df = pd.DataFrame({
        "Age": [
            20,
            21,
            22,
            23,
            24,
            1000
        ]
    })

    handler = OutlierHandler(df)

    result = handler.detect_zscore(
        "Age"
    )

    assert result is not None

    assert result["column"] == "Age"

    assert "mean" in result

    assert "std" in result

    assert "threshold" in result

    assert "outlier_count" in result


def test_iqr_analysis():

    df = pd.DataFrame({
        "Age": [
            20,
            21,
            22,
            23,
            24,
            1000
        ],

        "Salary": [
            30000,
            32000,
            35000,
            36000,
            38000,
            1000000
        ]
    })

    handler = OutlierHandler(df)

    result = handler.analyze_iqr()

    assert result is not None

    assert not result.empty

    assert "column" in result.columns

    assert "iqr" in result.columns

    assert "outlier_count" in result.columns


def test_zscore_analysis():

    df = pd.DataFrame({
        "Age": [
            20,
            21,
            22,
            23,
            24,
            1000
        ],

        "Salary": [
            30000,
            32000,
            35000,
            36000,
            38000,
            1000000
        ]
    })

    handler = OutlierHandler(df)

    result = handler.analyze_zscore()

    assert result is not None

    assert not result.empty

    assert "column" in result.columns

    assert "mean" in result.columns

    assert "std" in result.columns

    assert "outlier_count" in result.columns