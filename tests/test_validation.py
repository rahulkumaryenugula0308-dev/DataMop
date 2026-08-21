import pandas as pd
import pytest

from datamop.validation import (
    DataValidator
)

from datamop.exceptions import (
    DataMopInputError,
    DataMopDataError,
    DataMopConfigurationError
)


def test_valid_dataframe(
    sample_dataframe
):

    result = (
        DataValidator.validate_input(
            sample_dataframe
        )
    )

    assert result == "dataframe"


def test_invalid_input():

    with pytest.raises(
        DataMopInputError
    ):

        DataValidator.validate_input(
            12345
        )


def test_empty_dataframe():

    df = pd.DataFrame()

    with pytest.raises(
        DataMopDataError
    ):

        DataValidator.validate_dataframe(
            df
        )


def test_invalid_outlier_method():

    with pytest.raises(
        DataMopConfigurationError
    ):

        DataValidator.validate_outlier_method(
            "wrong"
        )


def test_valid_outlier_method():

    assert (
        DataValidator.validate_outlier_method(
            "iqr"
        )
        == "iqr"
    )

    assert (
        DataValidator.validate_outlier_method(
            "zscore"
        )
        == "zscore"
    )