import click
from ancientMetagenomeDirCheck import __version__
from ancientMetagenomeDirCheck.test_dataset.main import run_tests
from ancientMetagenomeDirCheck.filter.run_streamlit import run_app
from pathlib import Path


@click.group()
@click.version_option(__version__)
def cli(no_args_is_help=True, **kwargs):
    """\b
    ancientMetagenomeDirCheck: Performs validity check of ancientMetagenomeDir datasets
    Author: Maxime Borry
    Contact: <maxime_borry[at]eva.mpg.de>
    Homepage & Documentation: github.com/spaam-workshop/ancientMetagenomeDirCheck
    \b
    DATASET: path to tsv file of dataset to check
    SCHEMA: path to JSON schema file
    """
    pass


@cli.command()
@click.argument("dataset", type=click.Path(exists=True))
@click.argument("schema", type=click.Path(exists=True))
@click.option("-v", "--validity", is_flag=True, help="Turn on schema checking.")
@click.option(
    "-d", "--duplicate", is_flag=True, help="Turn on line duplicate line checking."
)
@click.option("-i", "--doi", is_flag=True, help="Turn on DOI duplicate checking.")
@click.option("-m", "--markdown", is_flag=True, help="Output is in markdown format")
@click.option(
    "-dc",
    "--duplicated_entries",
    type=str,
    help="Commma separated list of columns to check for duplicated entries",
)
def test_dataset(no_args_is_help=True, **kwargs):
    """\b
    Run validity check of ancientMetagenomeDir datasets
    \b
    DATASET: path to tsv file of dataset to check
    SCHEMA: path to JSON schema file
    """
    run_tests(**kwargs)


@cli.command()
@click.option("-c", "--config", type=click.Path(exists=True), help="Config file to use")
def filter(no_args_is_help=True, **kwargs):
    """Launch interactive filtering tool"""
    run_app(**kwargs)


if __name__ == "__main__":
    cli()
