from pathlib import Path


class Config:
    GATING = Path("./Table_BM_Trumpp.csv")
    CELL_COUNTS = Path("./cell_counts.csv")
    OUTPUT_DIR = Path.cwd()
    start_pop = "coi/db/lin-"
    order = ["B", "S"]
    organ = "BM lin-"
    power = "6"
    part_to_remove = "_1_001.fcs"
    stat_ind = "yes"
    single_comp = "no"
    control_group = "BM_all"
    stat_test = "t-test_welch"
    datatype = "png"
    size = 300
