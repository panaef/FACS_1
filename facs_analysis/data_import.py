import pandas as pd

from config import Config


class BMImport:
    def __init__(self):
        self.config = Config()

        self.bm_gating_df = pd.read_csv(
            self.config.GATING, sep=";", index_col=0)
        self.bm_gating_drop_names = ["Mean", "SD"]
        self.bm_gating_drop_indices = [0, 1]

        self.clean_data()
        self.clean_headings()
        self.drop_non_required()

    def clean_data(self):
        self.bm_gating_df = self.bm_gating_df.astype(str)
        for column in self.bm_gating_df:
            self.bm_gating_df[column] = self.bm_gating_df[column].str.replace("%", "")
            self.bm_gating_df[column] = self.bm_gating_df[column].apply(pd.to_numeric)
            self.bm_gating_df[column] = self.bm_gating_df[column] / 100

    def clean_headings(self):
        new_heading_map = {heading: heading.replace("Freq. of Parent", "")
                           for heading in self.bm_gating_df.columns}
        self.bm_gating_df.rename(columns=new_heading_map, inplace=True)
        self.bm_gating_df.columns = self.bm_gating_df.columns.str.replace(" ", "")
        self.bm_gating_df.columns = self.bm_gating_df.columns.str.replace(",", "")
        self.bm_gating_df.columns = self.bm_gating_df.columns.str.replace(":", "_")
        self.bm_gating_df.columns = self.bm_gating_df.columns.str.replace("|", "")

    def drop_non_required(self):
        self.bm_gating_df.drop(self.bm_gating_drop_names, inplace=True)
        self.bm_gating_df.drop([self.bm_gating_df.columns[i] for i in self.bm_gating_drop_indices], axis=1, inplace=True)
