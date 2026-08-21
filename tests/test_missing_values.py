from datamop.missing_values import (
    MissingValueHandler
)


def test_missing_values_are_detected(
    dataframe_with_missing_values
):

    handler = MissingValueHandler(
        dataframe_with_missing_values
    )

    result = handler.detect()

    assert result is not None


def test_total_missing_values(
    dataframe_with_missing_values
):

    handler = MissingValueHandler(
        dataframe_with_missing_values
    )

    result = (
        handler.total_missing_values()
    )

    assert result > 0