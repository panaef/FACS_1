from pathlib import Path


class Config:
    CELL_COUNTS = Path("./cell_counts.csv")
    OUTPUT_DIR = Path.cwd()
    start_pop = "coi/db/lin-"
    order = ["B", "S"]
    organ = "BM lin-"
    power = "6"
    stat_ind = "yes"
    single_comp = "no"
    control_group = "BM_all"
    stat_test = "t-test_welch"
    datatype = "png"
    size = 300

    def __init__(self, gating_path, part_to_remove):
        self.GATING = Path(gating_path)
        self.part_to_remove = part_to_remove