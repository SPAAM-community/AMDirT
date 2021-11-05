import click
from ancientMetagenomeDirCheck import __version__
from ancientMetagenomeDirCheck.main import run_tests
from pathlib import Path


@click.command()
@click.version_option(__version__)
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
def cli(no_args_is_help=True, **kwargs):
    """\b
    ancientMetagenomeDirCheck: Performs validity check of ancientMetagenomeDir datasets
    Author: Maxime Borry
    Contact: <borry[at]shh.mpg.de>
    Homepage & Documentation: github.com/spaam-workshop/ancientMetagenomeDirCheck
    \b
    DATASET: path to tsv file of dataset to check
    SCHEMA: path to JSON schema file
    """
    run_tests(**kwargs)


if __name__ == "__main__":
    cli()
