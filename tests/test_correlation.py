from datamop.correlation import (
    CorrelationAnalyzer
)


def test_correlation_matrix(
    sample_dataframe
):

    analyzer = CorrelationAnalyzer(
        sample_dataframe
    )

    result = analyzer.calculate()

    assert result is not None


def test_id_columns_are_excluded(
    sample_dataframe
):

    analyzer = CorrelationAnalyzer(
        sample_dataframe
    )

    columns = (
        analyzer.get_correlation_columns()
    )

    assert "ID" not in columns