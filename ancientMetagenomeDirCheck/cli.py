import click
from ancientMetagenomeDirCheck import __version__
from ancientMetagenomeDirCheck.main import run_tests
from pathlib import Path


@click.command()
@click.version_option(__version__)
@click.argument("dataset", type=click.Path(exists=True))
@click.argument("schema", type=click.Path(exists=True))
def cli(no_args_is_help=True, **kwargs):
    """\b
    ancientMetagenomeDirCheck: Performs validity check of ancientMetagenomeDir datasets
    Author: Maxime Borry
    Contact: <borry[at]shh.mpg.de>
    Homepage & Documentation: github.com/maxibor/ancientMetagenomeDirCheck
    \b
    DATASET: path to tsv file of dataset to check
    SCHEMA: path to JSON schema file
    """
    run_tests(**kwargs)


if __name__ == "__main__":
    cli()
