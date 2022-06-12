from pathlib import Path

from facs_analysis.config import Config
from facs_analysis.data_import import BMImport
from facs_analysis.data_percentage import DataPercentage


def test_init_config():
    gating_path = "./tests/assets/test_import_data.csv"
    cell_count = "./tests/assets/test_cell_count.csv"
    part_to_remove = "_1_001.fcs"
    config = Config(
        gating_path=gating_path,
        cell_count=cell_count,
        part_to_remove=part_to_remove
    )

    assert isinstance(config, Config)
    assert "test_import_data.csv" in config.GATING.as_posix()
    assert "test_cell_count.csv" in config.CELL_COUNTS.as_posix()


def test_init_bm_import(test_config):
    # expected first line of DF for the test data
    expected_cleaned_data = {'coi/db/lin-': {'B_1_001.fcs': 0.493}, 'coi/db/lin-/LSK': {'B_1_001.fcs': 0.0111}, 'coi/db/lin-/LSK/Q1_CD48-CD150+': {'B_1_001.fcs': 0.113}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/LT-HSC': {'B_1_001.fcs': 0.276}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/Q1_CD34-CD135+': {'B_1_001.fcs': 0.0}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/Q2_CD34+CD135+': {'B_1_001.fcs': 0.0}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/ST-HSC': {'B_1_001.fcs': 0.7240000000000001}, 'coi/db/lin-/LSK/Q2_CD48+CD150+': {'B_1_001.fcs': 0.0662}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/MPP1': {'B_1_001.fcs': 0.9420000000000001}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/Q1_CD34-CD135+': {'B_1_001.fcs': 0.0097}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/Q2_CD34+CD135+': {'B_1_001.fcs': 0.0}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/Q4_CD34-CD135-': {'B_1_001.fcs': 0.048499999999999995}, 'coi/db/lin-/LSK/Q3_CD48+CD150-': {'B_1_001.fcs': 0.742}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/MPP2': {'B_1_001.fcs': 0.446}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/MPP3': {'B_1_001.fcs': 0.51}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/Q1_CD34-CD135+': {'B_1_001.fcs': 0.0268}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/Q4_CD34-CD135-': {'B_1_001.fcs': 0.0169}, 'coi/db/lin-/LSK/Q4_CD48-CD150-': {'B_1_001.fcs': 0.0784}}

    bm_import = BMImport(config=test_config)
    # the actual first line of the cleaned data
    actual_cleaned_data = bm_import.bm_gating_df.iloc[:1].to_dict()

    assert actual_cleaned_data == expected_cleaned_data


def test_init_data_cleaning(test_config):
    bm_import = BMImport(config=test_config)
    expected_result_data = {'coi/db/lin-': {'B_1_001.fcs': 100}, 'coi/db/lin-/LSK': {'B_1_001.fcs': 1.11}, 'coi/db/lin-/LSK/Q1_CD48-CD150+': {'B_1_001.fcs': 0.12543}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/LT-HSC': {'B_1_001.fcs': 0.034618680000000006}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/Q1_CD34-CD135+': {'B_1_001.fcs': 0.0}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/Q2_CD34+CD135+': {'B_1_001.fcs': 0.0}, 'coi/db/lin-/LSK/Q1_CD48-CD150+/ST-HSC': {'B_1_001.fcs': 0.09081132000000001}, 'coi/db/lin-/LSK/Q2_CD48+CD150+': {'B_1_001.fcs': 0.073482}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/MPP1': {'B_1_001.fcs': 0.06922004400000001}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/Q1_CD34-CD135+': {'B_1_001.fcs': 0.0007127754}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/Q2_CD34+CD135+': {'B_1_001.fcs': 0.0}, 'coi/db/lin-/LSK/Q2_CD48+CD150+/Q4_CD34-CD135-': {'B_1_001.fcs': 0.003563877}, 'coi/db/lin-/LSK/Q3_CD48+CD150-': {'B_1_001.fcs': 0.82362}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/MPP2': {'B_1_001.fcs': 0.36733452}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/MPP3': {'B_1_001.fcs': 0.42004620000000004}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/Q1_CD34-CD135+': {'B_1_001.fcs': 0.022073016}, 'coi/db/lin-/LSK/Q3_CD48+CD150-/Q4_CD34-CD135-': {'B_1_001.fcs': 0.013919177999999999}, 'coi/db/lin-/LSK/Q4_CD48-CD150-': {'B_1_001.fcs': 0.087024}}

    data_percentage = DataPercentage(config=test_config, data=bm_import.bm_gating_df)
    actual_result_data = data_percentage.results.iloc[:1].to_dict()

    assert actual_result_data == expected_result_data
    # check the output file is being created
    assert Path("./results_percentage.csv").is_file()
