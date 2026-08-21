from datamop.profiler import ColumnProfiler


def test_profiler_creates_profile(
    sample_dataframe
):

    profiler = ColumnProfiler(
        sample_dataframe
    )

    result = profiler.profile()

    assert result is not None

    assert len(result) == (
        len(sample_dataframe.columns)
    )


def test_profiler_detects_id(
    sample_dataframe
):

    profiler = ColumnProfiler(
        sample_dataframe
    )

    result = profiler.profile_column(
        "ID"
    )

    assert result["column_type"] == "id"


def test_profiler_detects_continuous_numeric():

    import pandas as pd

    df = pd.DataFrame({
        "Salary": [
            30125.50,
            32450.75,
            35200.25,
            37850.90,
            40125.40,
            42500.60,
            44750.80,
            47200.35,
            49850.95,
            52300.45,
            54800.20,
            57250.70
        ]
    })

    profiler = ColumnProfiler(
        df
    )

    result = profiler.profile_column(
        "Salary"
    )

    assert result["column_type"] == (
        "numeric_continuous"
    )

    assert result["unique"] == 12

    assert result["rows"] == 12