import pandas as pd

from facs_analysis.config import Config


class DataPercentage:
    def __init__(self, config, data):
        self.data = data
        self.config = config
        self.results = None

        self.loop_data_multiplying_with_previous_cols()
        self.save_file()

    def loop_data_multiplying_with_previous_cols(self):
        self.results = pd.DataFrame()
        self.results[self.config.start_pop] = self.data[self.data.columns[0]]
        self.results[self.config.start_pop] = 100

        previous_col_name = self.config.start_pop
        concat_column_names = []

        for column_name in self.data:
            if previous_col_name in column_name:
                if column_name == self.config.start_pop:
                    concat_column_names.append(column_name)
                else:
                    self.results[column_name] = self.results[previous_col_name] * self.data[column_name]
                    previous_col_name = str(column_name)
                    concat_column_names.append(column_name)
            else:
                working_list = []
                for element in concat_column_names:
                    if element in column_name:
                        working_list.append(element)
                if len(working_list) == 0:
                    print(working_list)
                else:
                    max_value = max(working_list, key=len)
                    self.results[column_name] = self.results[max_value] * self.data[column_name]
                    previous_col_name = str(column_name)
                    concat_column_names.append(column_name)

    def save_file(self, filename="results_percentage.csv"):
        self.results.to_csv(self.config.OUTPUT_DIR / filename)
