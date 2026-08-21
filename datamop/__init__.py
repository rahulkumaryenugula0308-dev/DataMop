"""
DataMop
=======

Automatic data analysis, cleaning,
visualization and reporting library.
"""
import os
import pandas as pd

from datamop.pipeline import DataMopPipeline
from datamop.visualization import DataVisualizer

__version__ = "0.2.0"


# ======================================================
# ANALYZE
# ======================================================

def analyze(
    data,
    output_dir="datamop_output"
):
    """
    Analyze a dataset without modifying it.

    Parameters
    ----------
    data : str or pandas.DataFrame
        CSV/Excel path or DataFrame.

    Returns
    -------
    dict
        Analysis results.
    """

    pipeline = DataMopPipeline(
        output_dir=output_dir
    )

    pipeline._load_input(data)

    result = (
        pipeline.cleaner.analyze()
    )

    return {
        "dataframe":
            pipeline.cleaner.get_dataframe(),

        "analysis":
            result
    }


# ======================================================
# CLEAN
# ======================================================

def clean(
    data,
    remove_duplicates=True,
    handle_missing=True,
    remove_outliers=False,
    convert_datatypes=True,
    outlier_method="iqr",
    output_dir="datamop_output"
):
    """
    Clean a dataset automatically.

    Returns cleaned DataFrame and output files.
    """

    pipeline = DataMopPipeline(
        output_dir=output_dir
    )

    pipeline._load_input(data)

    pipeline.cleaner.clean(
        remove_duplicates=(
            remove_duplicates
        ),
        handle_missing=(
            handle_missing
        ),
        remove_outliers=(
            remove_outliers
        ),
        convert_datatypes=(
            convert_datatypes
        ),
        outlier_method=(
            outlier_method
        )
    )

    cleaned_df = (
        pipeline.cleaner.get_dataframe()
    )

    return {
        "dataframe":
            cleaned_df,

        "cleaning_log":
            pipeline.cleaner.get_cleaning_log()
    }


# ======================================================
# VISUALIZE
# ======================================================

def visualize(
    data,
    output_dir="datamop_output"
):
    """
    Automatically generate visualizations.
    """

    pipeline = DataMopPipeline(
        output_dir=output_dir
    )

    dataset_name = (
        pipeline._load_input(data)
    )

    dataframe = (
        pipeline.cleaner.get_dataframe()
    )

    visualization_dir = os.path.join(
        output_dir,
        "visualizations",
        dataset_name
    )

    visualizer = DataVisualizer(
        dataframe,
        output_dir=visualization_dir
    )

    files = (
        visualizer.generate_all()
    )

    return {
        "dataframe":
            dataframe,

        "visualizations":
            files
    }


# ======================================================
# AUTO CLEAN
# ======================================================

def auto_clean(
    data,
    remove_duplicates=True,
    handle_missing=True,
    remove_outliers=False,
    convert_datatypes=True,
    outlier_method="iqr",
    output_dir="datamop_output"
):
    """
    Run the complete DataMop pipeline.

    Workflow:

        Load
        ↓
        Analyze
        ↓
        Clean
        ↓
        Visualize
        ↓
        Save
        ↓
        Report
    """

    pipeline = DataMopPipeline(
        output_dir=output_dir
    )

    return pipeline.run(
        data=data,
        remove_duplicates=(
            remove_duplicates
        ),
        handle_missing=(
            handle_missing
        ),
        remove_outliers=(
            remove_outliers
        ),
        convert_datatypes=(
            convert_datatypes
        ),
        outlier_method=(
            outlier_method
        )
    )