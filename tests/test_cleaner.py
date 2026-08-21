from datamop.cleaner import DataCleaner


def test_cleaner_initialization():

    cleaner = DataCleaner()

    assert cleaner is not None


def test_cleaner_loads_dataframe(
    sample_dataframe
):

    cleaner = DataCleaner()

    cleaner.df = (
        sample_dataframe.copy()
    )

    assert cleaner.df is not None

    assert len(
        cleaner.df
    ) == 5