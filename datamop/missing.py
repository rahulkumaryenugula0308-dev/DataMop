import pandas as pd


def detect_missing(df):
    return df.isnull().sum()


def fill_mean(df):
    return df.fillna(df.mean(numeric_only=True))


def fill_median(df):
    return df.fillna(df.median(numeric_only=True))


def fill_mode(df):
    result = df.copy()

    for column in result.columns:
        if result[column].isnull().any():
            mode = result[column].mode()

            if not mode.empty:
                result[column] = result[column].fillna(mode.iloc[0])

    return result


def fill_constants(df, value="Unknown"):
    return df.fillna(value)


def drop_missing(df):
    return df.dropna()


def forward_fill(df):
    return df.ffill()


def backward_fill(df):
    return df.bfill()


def drop_columns_by_missing(df, threshold=40):
    missing_percent = (df.isnull().sum() / len(df)) * 100

    columns_to_drop = missing_percent[
        missing_percent > threshold
    ].index

    return df.drop(columns=columns_to_drop)


def clean_missing_values(
    df,
    threshold=40,
    numeric_method="mean",
    categorical_method="mode",
    fill_value="Unknown"
):
    """
    Main missing-value cleaning function.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    threshold : int or float
        Columns with missing values greater than this
        percentage will be removed.

    numeric_method : str
        Method for numeric columns:
        "mean", "median", or "constant".

    categorical_method : str
        Method for text/categorical columns:
        "mode" or "constant".

    fill_value : any
        Value used when constant filling is selected.

    Returns
    -------
    pandas.DataFrame
        Cleaned DataFrame.
    """

    cleaned_df = df.copy()

    # --------------------------------------------------
    # Step 1: Remove columns with too many missing values
    # --------------------------------------------------

    missing_percent = (
        cleaned_df.isnull().sum() / len(cleaned_df)
    ) * 100

    columns_to_drop = missing_percent[
        missing_percent > threshold
    ].index

    cleaned_df = cleaned_df.drop(
        columns=columns_to_drop
    )

    # --------------------------------------------------
    # Step 2: Handle numeric columns
    # --------------------------------------------------

    numeric_columns = cleaned_df.select_dtypes(
        include="number"
    ).columns

    if numeric_method == "mean":

        cleaned_df[numeric_columns] = (
            cleaned_df[numeric_columns]
            .fillna(
                cleaned_df[numeric_columns].mean()
            )
        )

    elif numeric_method == "median":

        cleaned_df[numeric_columns] = (
            cleaned_df[numeric_columns]
            .fillna(
                cleaned_df[numeric_columns].median()
            )
        )

    elif numeric_method == "constant":

        cleaned_df[numeric_columns] = (
            cleaned_df[numeric_columns]
            .fillna(fill_value)
        )

    else:
        raise ValueError(
            "numeric_method must be "
            "'mean', 'median', or 'constant'"
        )

    # --------------------------------------------------
    # Step 3: Handle categorical/text columns
    # --------------------------------------------------

    categorical_columns = cleaned_df.select_dtypes(
        exclude="number"
    ).columns

    if categorical_method == "mode":

        for column in categorical_columns:

            if cleaned_df[column].isnull().any():

                mode = cleaned_df[column].mode()

                if not mode.empty:
                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(mode.iloc[0])
                    )

    elif categorical_method == "constant":

        cleaned_df[categorical_columns] = (
            cleaned_df[categorical_columns]
            .fillna(fill_value)
        )

    else:
        raise ValueError(
            "categorical_method must be "
            "'mode' or 'constant'"
        )

    return cleaned_df