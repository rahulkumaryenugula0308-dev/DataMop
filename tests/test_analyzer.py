from datamop.analyzer import DataAnalyzer


def test_analyzer_summary(
    sample_dataframe
):

    analyzer = DataAnalyzer(
        sample_dataframe
    )

    result = analyzer.analyze()

    assert result is not None