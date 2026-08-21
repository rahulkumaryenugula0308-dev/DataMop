from datamop.datatype import DataTypeHandler


def test_datatype_handler(
    sample_dataframe
):

    handler = DataTypeHandler(
        sample_dataframe
    )

    result = handler.get_type_report()

    assert result is not None