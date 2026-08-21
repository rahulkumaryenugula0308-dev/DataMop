from datamop.duplicates import (
    DuplicateHandler
)


def test_duplicates_are_detected(
    duplicate_dataframe
):

    handler = DuplicateHandler(
        duplicate_dataframe
    )

    result = handler.detect()

    assert result is not None