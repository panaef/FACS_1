import pytest

from facs_analysis.config import Config


@pytest.fixture()
def test_config():
    gating_path = "./tests/assets/test_import_data.csv"
    cell_count = "./tests/assets/test_cell_count.csv"
    part_to_remove = "_1_001.fcs"
    config = Config(
        gating_path=gating_path,
        cell_count=cell_count,
        part_to_remove=part_to_remove
    )
    yield config
