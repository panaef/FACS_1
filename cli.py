import click

from facs_analysis.config import Config
from facs_analysis.data_import import BMImport
from facs_analysis.data_percentage import DataPercentage
from facs_analysis.data_visualizer import DataVisualizer


@click.command()
@click.option("--gatingpath", prompt="Gating Path",
              help="...")
@click.option("--cellcount", prompt="Cell count",
              help="...")
@click.option("--parttoremove", prompt="Part to remove",
              help="...")
def facs(gating_path, cell_count, part_to_remove):
    """Runs the facs routine."""
    config = Config(
        gating_path=gating_path,
        cell_count=cell_count,
        part_to_remove=part_to_remove
    )
    bm_import = BMImport(config=config)
    data_percentage = DataPercentage(config=config, data=bm_import.bm_gating_df)
    visualizer = DataVisualizer(config=config, data=bm_import.bm_gating_df, results=data_percentage.results)
    visualizer.plot_percentage_of_total()
    visualizer.plot_absolute_counts()


if __name__ == '__main__':
    facs()
