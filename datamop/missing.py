"""
=========================================================
missing.py
=========================================================

Purpose:
--------
This module contains all functions related to handling
missing (NaN) values in a dataset.

Author : Rahul
Project: DataMop

=========================================================
"""

# -------------------------------------------------------
# Import Required Library
# -------------------------------------------------------

import pandas as pd


# =======================================================
# 1. Detect Missing Values
# =======================================================
def detect_missing(df):
    """
    Count missing values in every column.

    Detects:
    - NaN
    - None
    - N/A
    - ?
    - -
    - Unknown
    - Blank cells
    """

    # Create a copy so the original DataFrame is not modified
    temp_df = df.copy()

    # Replace common missing value representations with Pandas NA
    temp_df = temp_df.replace(
        [
            "N/A",
            "n/a",
            "?",
            "-",
            "Unknown",
            "unknown",
            "",
            " "
        ],
        pd.NA
    )

    # Return missing value count for each column
    return temp_df.isna().sum()

# =======================================================
# 2. Fill Numeric Missing Values Using Mean
# =======================================================

def fill_mean(df):
    """
    Fill missing values of numeric columns using Mean.

    Example:
        Age
        ----
        20
        NaN
        30

    Mean = 25

    Output:
        20
        25
        30
    """

    # Create a copy to protect original dataset
    new_df = df.copy()

    # Select only numeric columns
    numeric_columns = new_df.select_dtypes(include="number").columns

    # Replace NaN with column mean
    new_df[numeric_columns] = new_df[numeric_columns].fillna(
        new_df[numeric_columns].mean()
    )

    return new_df


# =======================================================
# 3. Fill Numeric Missing Values Using Median
# =======================================================

def fill_median(df):
    """
    Fill missing values using Median.

    Median is useful when data contains outliers.
    """

    new_df = df.copy()

    numeric_columns = new_df.select_dtypes(include="number").columns

    new_df[numeric_columns] = new_df[numeric_columns].fillna(
        new_df[numeric_columns].median()
    )

    return new_df


# =======================================================
# 4. Fill Missing Values Using Mode
# =======================================================

def fill_mode(df):
    """
    Fill missing values using Mode.

    Works for both:
    - Numeric columns
    - Text columns
    """

    new_df = df.copy()

    # Loop through every column
    for column in new_df.columns:

        # Check if column contains missing values
        if new_df[column].isnull().sum() > 0:

            # Get most frequent value
            mode_value = new_df[column].mode()

            # Fill missing values if mode exists
            if not mode_value.empty:
                new_df[column] = new_df[column].fillna(mode_value[0])

    return new_df


# =======================================================
# 5. Drop Rows Containing Missing Values
# =======================================================

def drop_missing(df):
    """
    Remove all rows that contain at least one missing value.
    """

    return df.dropna()


# =======================================================
# 6. Forward Fill
# =======================================================

def forward_fill(df):
    """
    Replace missing values using previous row value.

    Example

    20
    NaN
    NaN
    30

    becomes

    20
    20
    20
    30
    """

    return df.ffill()


# =======================================================
# 7. Backward Fill
# =======================================================

def backward_fill(df):
    """
    Replace missing values using next row value.

    Example

    20
    NaN
    NaN
    30

    becomes

    20
    30
    30
    30
    """

    return df.bfill()


# =======================================================
# 8. Drop Columns Having Too Many Missing Values
# =======================================================

def drop_columns_by_missing(df, threshold=40):
    """
    Remove columns whose missing percentage
    is greater than the threshold.

    Example

    Threshold = 40%

    Age = 20%
    Cabin = 77%

    Cabin will be removed.
    """

    # Calculate missing percentage
    missing_percentage = (df.isnull().sum() / len(df)) * 100

    print("=" * 50)
    print("Missing Percentage of Each Column")
    print("=" * 50)
    print(missing_percentage)

    # Find columns above threshold
    columns_to_drop = missing_percentage[
        missing_percentage > threshold
    ].index

    print("\nColumns Removed:")
    print(list(columns_to_drop))

    # Remove columns
    cleaned_df = df.drop(columns=columns_to_drop)

    return cleaned_df


# =======================================================
# 9. Complete Missing Value Cleaning Pipeline
# =======================================================

def clean_missing_values(df, threshold=40, numeric_method="mean"):
    """
    Complete missing value cleaning process.

    Steps:
    ------
    Step 1 -> Remove columns with too many missing values.

    Step 2 -> Fill numeric columns
              Mean OR Median.

    Step 3 -> Fill text columns using Mode.

    Returns
    -------
    Cleaned DataFrame
    """

    # -----------------------------
    # Step 1
    # Remove columns having too many NaN values
    # -----------------------------
    cleaned_df = drop_columns_by_missing(df, threshold)

    # -----------------------------
    # Step 2
    # Fill numeric values
    # -----------------------------
    if numeric_method.lower() == "mean":
        cleaned_df = fill_mean(cleaned_df)

    elif numeric_method.lower() == "median":
        cleaned_df = fill_median(cleaned_df)

    # -----------------------------
    # Step 3
    # Fill categorical columns
    # -----------------------------
    cleaned_df = fill_mode(cleaned_df)

    return cleaned_df
# ----------------------------------------------------------
# 10. Fill Missing Values with a Constant Value
# ----------------------------------------------------------

def fill_constant(df, value="Unknown"):
    """
    Fill all missing values with a constant value.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    value : str or int or float
        Value used to replace missing values.

    Returns
    -------
    pandas.DataFrame
        DataFrame after filling missing values.
    """

    # Create a copy so the original DataFrame is not modified
    cleaned_df = df.copy()

    # Replace common missing value representations with Pandas NA
    cleaned_df = cleaned_df.replace(
        [
            "N/A",
            "n/a",
            "?",
            "-",
            "Unknown",
            "unknown",
            "",
            " "
        ],
        pd.NA
    )

    # Fill all missing values
    cleaned_df = cleaned_df.fillna(value)

    return cleaned_df