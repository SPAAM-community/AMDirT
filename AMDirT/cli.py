import json
import click
from AMDirT import __version__
from AMDirT.test_dataset.main import run_tests
from AMDirT.filter.run_streamlit import run_app
from AMDirT.convert.main import run_convert
from AMDirT.core.utils import get_json_path
from json import load
from pathlib import Path


def get_table_list():
    json_path = get_json_path()
    print(json_path)
    with open(json_path, "r") as f:
        table_list = load(f)
        return table_list["samples"].keys()


@click.group()
@click.version_option(__version__)
def cli(no_args_is_help=True, **kwargs):
    """\b
    AMDirT: Performs validity check of ancientMetagenomeDir datasets
    Authors: Maxime Borry, Jasmin Frangenberg, Nikolay Oskolov
    Contact: <maxime_borry[at]eva.mpg.de>
    Homepage & Documentation: https://github.com/SPAAM-community/AMDirT
    \b
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
@click.option(
    "-t",
    "--tables",
    type=click.Path(exists=True),
    help="JSON file listing AncientMetagenomeDir tables",
)
def filter(no_args_is_help=True, **kwargs):
    """Launch interactive filtering tool"""
    run_app(**kwargs)


@cli.command()
@click.argument("samples", type=click.Path(exists=True))
@click.argument("table_name", type=str)
@click.option(
    "-t",
    "--tables",
    type=click.Path(exists=True),
    help="(Optional) JSON file listing AncientMetagenomeDir tables",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(writable=True, dir_okay=True, file_okay=False),
    default=".",
    show_default=True,
    help="conversion output directory",
)
def convert(no_args_is_help=True, **kwargs):
    """\b
    Converts filtered samples and libraries tables to eager and fetchNGS input tables
    \b
    SAMPLES: path to filtered ancientMetagenomeDir samples tsv file
    TABLE_NAME: name of table to convert
    """
    run_convert(**kwargs)


if __name__ == "__main__":
    cli()
