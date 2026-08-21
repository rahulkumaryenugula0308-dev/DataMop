import os

from datamop.visualization import (
    DataVisualizer
)


def test_visualization_generation(
    sample_dataframe,
    tmp_path
):

    output_dir = (
        tmp_path /
        "visualizations"
    )

    visualizer = DataVisualizer(
        sample_dataframe,
        output_dir=str(
            output_dir
        )
    )

    result = (
        visualizer.generate_all()
    )

    assert result is not None

    assert isinstance(
        result,
        list
    )

    assert len(result) > 0

    for filepath in result:

        assert os.path.exists(
            filepath
        )