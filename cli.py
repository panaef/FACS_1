import click

from facs_analysis.data_import import BMImport
from facs_analysis.data_percentage import DataPercentage


@click.command()
@click.option("--example-option", prompt="Example Option",
              help="Some help for the example option.")
def facs(example_option):
    """Runs the facs routine."""
    bm_import = BMImport()
    data_percentage = DataPercentage(bm_import.bm_gating_df)


if __name__ == '__main__':
    facs()
