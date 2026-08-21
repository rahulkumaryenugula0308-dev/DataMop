import pandas as pd

import datamop


def test_analyze(
    sample_dataframe
):

    result = datamop.analyze(
        sample_dataframe
    )

    assert isinstance(
        result,
        dict
    )

    assert "dataframe" in result

    assert "analysis" in result


def test_clean(
    sample_dataframe
):

    result = datamop.clean(
        sample_dataframe
    )

    assert isinstance(
        result,
        dict
    )

    assert "dataframe" in result

    assert "cleaning_log" in result