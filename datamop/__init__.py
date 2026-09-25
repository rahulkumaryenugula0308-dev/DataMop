"""
DataMop
-------

Automatic data cleaning, analysis, visualization
and reporting library.
"""

from datamop.pipeline import DataMopPipeline
from datamop.visualization import DataVisualizer


__version__ = "0.2.0"


# ==================================================
# Analyze
# ==================================================

def analyze(
    data,
    output_dir="datamop_output"
):
    """
    Analyze a CSV, Excel file, or pandas DataFrame.

    Returns a dictionary containing:
    - analysis
    - dataframe
    """

    pipeline = DataMopPipeline(
        output_dir=output_dir
    )

    pipeline._load_input(data)

    analysis_result = pipeline.cleaner.analyze()

    result = {
        "analysis": analysis_result,
        "dataframe": pipeline.cleaner.get_dataframe()
    }

    return result


# ==================================================
# Clean
# ==================================================

def clean(
    data,
    remove_duplicates=True,
    handle_missing=True,
    remove_outliers=False,
    convert_datatypes=True,
    outlier_method="iqr",
    missing_threshold=40,
    standardize_text=True,
    text_case="lower",
    normalize_categories=True,
    output_dir="datamop_output"
):
    """
    Clean a CSV, Excel file, or pandas DataFrame.

    Parameters
    ----------
    data : str or pandas.DataFrame
        Input dataset.

    remove_duplicates : bool
        Remove duplicate rows.

    handle_missing : bool
        Handle missing values.

    remove_outliers : bool
        Remove numerical outliers.

    convert_datatypes : bool
        Automatically convert data types.

    outlier_method : str
        'iqr' or 'zscore'.

    missing_threshold : float
        Columns with missing values greater than
        this percentage are removed.

    standardize_text : bool
        Standardize text and categorical values.

    text_case : str
        'lower', 'upper', or 'title'.

    normalize_categories : bool
        Normalize category labels.

    output_dir : str
        Directory for DataMop outputs.

    Returns
    -------
    dict
        DataMop processing result.
    """

    pipeline = DataMopPipeline(
        output_dir=output_dir
    )

    result = pipeline.run(
        data=data,
        remove_duplicates=remove_duplicates,
        handle_missing=handle_missing,
        remove_outliers=remove_outliers,
        convert_datatypes=convert_datatypes,
        outlier_method=outlier_method,
        missing_threshold=missing_threshold,
        standardize_text=standardize_text,
        text_case=text_case,
        normalize_categories=normalize_categories
    )

    # Backward compatibility
    result["dataframe"] = result["cleaned_dataframe"]

    return result


# ==================================================
# Visualize
# ==================================================

def visualize(
    data,
    output_dir="datamop_output"
):
    """
    Generate visualizations for a dataset.
    """

    visualizer = DataVisualizer(
        data,
        output_dir=output_dir
    )

    return visualizer.generate_all()


# ==================================================
# Auto Clean
# ==================================================

def auto_clean(
    data,
    remove_duplicates=True,
    handle_missing=True,
    remove_outliers=False,
    convert_datatypes=True,
    outlier_method="iqr",
    missing_threshold=40,
    standardize_text=True,
    text_case="lower",
    normalize_categories=True,
    output_dir="datamop_output"
):
    """
    Automatically clean and process a dataset.
    """

    return clean(
        data=data,
        remove_duplicates=remove_duplicates,
        handle_missing=handle_missing,
        remove_outliers=remove_outliers,
        convert_datatypes=convert_datatypes,
        outlier_method=outlier_method,
        missing_threshold=missing_threshold,
        standardize_text=standardize_text,
        text_case=text_case,
        normalize_categories=normalize_categories,
        output_dir=output_dir
    )


# ==================================================
# Public API
# ==================================================

__all__ = [
    "DataMopPipeline",
    "DataVisualizer",
    "analyze",
    "clean",
    "visualize",
    "auto_clean"
]