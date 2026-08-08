import pandas as pd


def dataset_summary(df):
    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }


def numeric_summary(df):
    return df.describe(include="number")


def categorical_summary(df):
    return df.describe(include="object")


def summary(df):
    return {
        "dataset": dataset_summary(df),
        "numeric": numeric_summary(df),
        "categorical": categorical_summary(df)
    }