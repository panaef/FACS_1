from pathlib import Path


class Config:
    OUTPUT_DIR = Path(Path.cwd(), "out")
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

    def __init__(self, gating_path, cell_count, part_to_remove):
        self.GATING = Path(gating_path)
        self.CELL_COUNTS = Path(cell_count)
        self.part_to_remove = part_to_remove
