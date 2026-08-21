from datamop.pipeline import (
    DataMopPipeline
)


def test_pipeline_runs(
    sample_dataframe,
    tmp_path
):

    output_dir = (
        tmp_path /
        "datamop_output"
    )

    pipeline = DataMopPipeline(
        output_dir=str(
            output_dir
        )
    )

    result = pipeline.run(
        sample_dataframe
    )

    assert isinstance(
        result,
        dict
    )

    assert (
        "cleaned_dataframe"
        in result
    )

    assert (
        "cleaned_file"
        in result
    )

    assert (
        "report"
        in result
    )

    assert (
        "visualizations"
        in result
    )