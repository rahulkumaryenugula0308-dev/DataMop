import pandas as pd

from datamop.loader import DataLoader


def test_loader_loads_csv(
    tmp_path
):

    filepath = (
        tmp_path /
        "test.csv"
    )

    df = pd.DataFrame({
        "Name": [
            "Alice",
            "Bob"
        ],

        "Age": [
            25,
            30
        ]
    })

    df.to_csv(
        filepath,
        index=False
    )

    loader = DataLoader()

    result = loader.load(
        str(filepath)
    )

    assert isinstance(
        result,
        pd.DataFrame
    )

    assert len(result) == 2

    assert list(
        result.columns
    ) == [
        "Name",
        "Age"
    ]