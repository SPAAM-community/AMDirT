import click
from AMDirT import __version__

from AMDirT.validate import run_validation
from AMDirT.viewer import run_app
from AMDirT.convert import run_convert
from AMDirT.core import get_json_path
from AMDirT.autofill import run_autofill
from json import load


def get_table_list():
    json_path = get_json_path()
    with open(json_path, "r") as f:
        table_list = load(f)
        return list(table_list["samples"].keys())


@click.group()
@click.version_option(__version__)
@click.pass_context
@click.option("--verbose", is_flag=True, help="Verbose mode")
def cli(ctx, verbose, no_args_is_help=True, **kwargs):
    """\b
    AMDirT: Performs validity check of ancientMetagenomeDir datasets
    Authors: AMDirT development team and the SPAAM community
    Homepage & Documentation: https://github.com/SPAAM-community/AMDirT
    \b
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    pass


####################
# Validation  tool #
####################


@cli.command()
@click.argument("dataset", type=click.Path(exists=True))
@click.argument("schema", type=click.Path(exists=True))
@click.option("-s", "--schema_check", is_flag=True, help="Turn on schema checking.")
@click.option(
    "-d", "--line_dup", is_flag=True, help="Turn on line duplicate line checking."
)
@click.option(
    "-c", "--columns", is_flag=True, help="Turn on column presence/absence checking."
)
@click.option("-i", "--doi", is_flag=True, help="Turn on DOI duplicate checking.")
@click.option(
    "--multi_values",
    multiple=True,
    help="Check multi-values column for duplicate values.",
)
@click.option(
    "-a",
    "--online_archive",
    is_flag=True,
    help="Turn on ENA accession validation",
)
@click.option(
    "--remote",
    type=click.Path(),
    default=None,
    help="[Optional] Path/URL to remote reference sample table for archive accession validation",
)
@click.option("-m", "--markdown", is_flag=True, help="Output is in markdown format")
@click.pass_context
def validate(ctx, no_args_is_help=True, **kwargs):
    """\b
    Run validity check of ancientMetagenomeDir datasets
    \b
    DATASET: path to tsv file of dataset to check
    SCHEMA: path to JSON schema file
    """
    run_validation(**kwargs, **ctx.obj)


###############################
# Interactive viewing/filtering  tool #
###############################


@cli.command()
@click.option(
    "-t",
    "--tables",
    type=click.Path(exists=True),
    help="JSON file listing AncientMetagenomeDir tables",
)
@click.pass_context
def viewer(ctx, no_args_is_help=True, **kwargs):
    """Launch interactive filtering tool"""
    run_app(**kwargs, **ctx.obj)


###################
# Conversion tool #
###################


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
    "--library_output",
    type=click.Path(writable=True, dir_okay=True, file_okay=False),
    default=".",
    show_default=True,
    help="conversion output directory",
)
@click.option(
    "--eager",
    is_flag=True,
    help="Convert filtered samples and libraries tables to eager input tables",
)
@click.option(
    "--fetchngs",
    is_flag=True,
    help="Convert filtered samples and libraries tables to fetchNGS input tables",
)
@click.option(
    "--ameta",
    is_flag=True,
    help="Convert filtered samples and libraries tables to aMeta input tables",
)
@click.option(
    "--mag",
    is_flag=True,
    help="Convert filtered samples and libraries tables to nf-core/mag input tables",
)
@click.pass_context
def convert(ctx, no_args_is_help=True, **kwargs):
    """\b
    Converts filtered samples and libraries tables to eager, ameta, and fetchNGS input tables
    \b
    SAMPLES: path to filtered ancientMetagenomeDir samples tsv file
    TABLE_NAME: name of table to convert
    """
    run_convert(**kwargs, **ctx.obj)


###################
# Autofill tool #
###################

@cli.command()
@click.option(
    "-a",
    "--accession",
    type=str, 
    multiple=True,
    help="ENA accession(s). Repeat for multiple accessions (e.g. -a PRJNA123 -a PRJNA456)"
)
@click.option(
    "-n",
    "--table_name", 
    type=click.Choice(get_table_list()),
    default='ancientmetagenome-hostassociated',
    show_default=True
)
@click.option(
    "-l",
    "--library_output",
    type=click.Path(writable=True),
    help="path to library output table file"
)
@click.option(
    "-s",
    "--sample_output",
    type=click.Path(writable=True),
    help="path to sample output table file"
)
@click.pass_context
def autofill(ctx, no_args_is_help=True, **kwargs):
    """\b
    Autofills library and/or sample table(s) using ENA API and accession numbers
    \b
    """
    run_autofill(**kwargs, **ctx.obj)


if __name__ == "__main__":
    cli()
