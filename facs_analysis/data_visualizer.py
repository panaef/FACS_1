import itertools
from pathlib import Path

from statannot import add_stat_annotation
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from facs_analysis.config import Config

# seaborn settings
sns.set_style("ticks")
sns.set_palette("Dark2")


class DataVisualizer:
    split = "/"

    def __init__(self, config: Config, data, results):
        self.config = config
        self.data = data
        self.results = results

        self.add_group()
        self.tuple_comp = self.get_group_information()

        self.visualize_data_one()

        self.count_table = self.calculate_absolute_counts()
        self.count_table_absolute = self.calculate_absolute_counts()

        self.visualize_absolute_counts()

    def add_group(self):
        self.results['group'] = self.results.index
        self.results["group"] = self.results["group"].str[
                                :-len(self.config.part_to_remove)]

    def get_group_information(self):
        pairs = self.results["group"].tolist()
        pairs = list(set(pairs))
        n_pairs = len(pairs)
        tuple_comp = []

        if self.config.stat_ind == "yes":
            if n_pairs <= 2:
                tuple_comp = [tuple(pairs)]
            elif self.config.single_comp == "yes":
                for pair in itertools.combinations(pairs, 2):
                    tuple_comp.append(pair)
                tuple_comp = [item for item in tuple_comp if
                              self.config.control_group in item]
            else:
                for pair in itertools.combinations(pairs, 2):
                    tuple_comp.append(pair)

        return tuple_comp

    def visualize_data_one(self):
        for column in self.results:
            if column != str("group"):
                ax = sns.catplot(
                    kind="bar",
                    data=self.results,
                    y=column,
                    x="group",
                    ci="sd",
                    edgecolor="black",
                    errcolor="black",
                    errwidth=1.5,
                    capsize=0.1,
                    alpha=0.3,
                    order=self.config.order)
                ax = sns.stripplot(x="group",
                                   y=column,
                                   data=self.results,
                                   dodge=True,
                                   alpha=1,
                                   linewidth=3,
                                   order=self.config.order)
                plt.xlabel(None)
                plt.ylabel((column.split(self.split)[
                                -1] + " (%of total " + self.config.organ + ")"),
                           fontsize=17)
                plt.title(column.split(self.split)[-1], fontsize=20)
                plt.xticks(rotation=45)
                plt.tick_params(axis='both', which='major', labelsize=14)

                if self.config.stat_ind == "yes":
                    add_stat_annotation(ax,
                                        data=self.results,
                                        x="group",
                                        y=column,
                                        order=self.config.order,
                                        box_pairs=self.tuple_comp,
                                        test=self.config.stat_test,
                                        text_format='star',
                                        loc='inside',
                                        verbose=2, fontsize=15)

                plt.savefig(
                    Path(self.config.OUTPUT_DIR, column.split(self.split)[
                        -1] + "_percentage_of_tot" + "." + self.config.datatype),
                    dpi=self.config.size,
                    bbox_inches="tight")

    def calculate_absolute_counts(self):
        count_table = pd.read_csv(
            self.config.CELL_COUNTS, sep=';', index_col=0)
        count_table = count_table.rename(
            columns={count_table.columns[0]: self.config.start_pop})
        count_table = self.results.merge(
            count_table, suffixes=("_results", "_count"), left_index=True,
            right_index=True)
        count_table = count_table[["coi/db/lin-_count"]]
        count_table = count_table.rename(columns=lambda x: str(x)[:-6])

        substring = self.config.start_pop
        stringlist = []
        count = 0

        # Iterate through the Percentage-Table (column by column)
        for column in self.data:

            if substring in column:  # check if my set substring is contained in the column name
                if column == self.config.start_pop:
                    stringlist.append(column)
                else:
                    count_table[column] = count_table[substring] * self.data[
                        column]  # if substring is part of column name, do the calculations
                    substring = str(
                        column)  # reset the variable "substring" with the column name
                    stringlist.append(
                        column)  # add the column name as an element to the stringlist
            else:  # if my column name is not contained in the previous column, the code continues here
                working_list = []  # create another empty list
                for element in stringlist:  # iterate over the stringlist (contains the names of all previous columns)
                    if element in column:  # if one of the previous columns is contained in the current column, the name will be added to the working_list
                        working_list.append(element)
                max_value = max(working_list,
                                key=len)  # create the variable "max_value", which contains the longest element form the working_list
                count_table[column] = count_table[max_value] * self.data[
                    column]  # use the max_value column name to calculate the value of the new column
                substring = str(column)
                stringlist.append(column)

        filepath = Path(self.config.OUTPUT_DIR, "results_absolute.csv")
        count_table.to_csv(filepath)
        return count_table

    def visualize_absolute_counts(self):
        self.count_table_absolute['group'] = self.count_table_absolute.index
        self.count_table_absolute["group"] = self.count_table_absolute[
                                                 "group"].str[
                                             :-len(self.config.part_to_remove)]

        for column in self.count_table_absolute:
            if column != str("group"):
                ax = sns.catplot(
                    kind="bar",
                    data=self.count_table_absolute,
                    y=column,
                    x="group",
                    ci="sd",
                    edgecolor="black",
                    errcolor="black",
                    errwidth=1.5,
                    capsize=0.1,
                    alpha=0.3,
                    order=self.config.order)
                ax = sns.stripplot(x="group",
                                   y=column,
                                   data=self.count_table_absolute,
                                   dodge=True,
                                   alpha=1,
                                   linewidth=3,
                                   order=self.config.order)
                plt.xlabel(None)
                plt.ylabel(
                    (self.config.organ + " " + column.split(self.split)[
                        -1] + " count [x10^" + self.config.power + "]"),
                    fontsize=17)
                plt.title(column.split(self.split)[-1], fontsize=20)
                plt.xticks(rotation=45)
                plt.tick_params(axis='both', which='major', labelsize=14)

                if self.config.stat_ind == "yes":
                    add_stat_annotation(ax,
                                        data=self.count_table_absolute,
                                        x="group",
                                        y=column,
                                        order=self.config.order,
                                        box_pairs=self.tuple_comp,
                                        test=self.config.stat_test,
                                        text_format='star',
                                        loc='inside',
                                        verbose=2, fontsize=15)

                plt.savefig(
                    Path(self.config.OUTPUT_DIR, column.split(self.split)[
                        -1] + "_absolute" + "." + self.config.datatype),
                    dpi=self.config.size, bbox_inches="tight")
