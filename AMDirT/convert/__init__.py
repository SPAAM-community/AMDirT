from sys import path
from AMDirT.core import (
    prepare_accession_table,
    prepare_bibtex_file,
    prepare_eager_table,
    prepare_aMeta_table,
    is_merge_size_zero,
)
from AMDirT.core import get_json_path
from json import load
from AMDirT.core import logger
import pandas as pd
import warnings


def run_convert(
    samples,
    tables,
    table_name,
    output=".",
    eager=False,
    fetchngs=False,
    ameta=False,
    verbose=False,
):
    """Run the AMDirT conversion application to input samplesheet tables for different pipelines

    Args:
        tables (str): Path to JSON file listing tables
        samples (str): Path to AncientMetagenomeDir filtered samples tsv file
        table_name (str): Name of the table of the table to convert
        output (str): Path to output table. Defaults to "."
    """
    if not verbose:
        warnings.filterwarnings("ignore")
    supported_archives = ["ENA", "SRA"]
    if tables is None:
        table_path = get_json_path()
    else:
        table_path = tables
    with open(table_path, "r") as f:
        tables = load(f)
    table_list = list(tables["samples"].keys())
    if table_name not in table_list:
        logger.info(f"Table '{table_name}' not found in {table_list}")
    samples = pd.read_csv(samples, sep="\t")
    libraries = pd.read_csv(tables["libraries"][table_name], sep="\t")

    if eager == True:
        logger.info("Preparing Eager table")
        eager_table = prepare_eager_table(
            samples=samples,
            libraries=libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )
        eager_table.to_csv(f"{output}/eager_input_table.tsv", sep="\t", index=False)

    if fetchngs == True:
        logger.info("Preparing FetchNGS table")
        accession_table = prepare_accession_table(
            samples=samples,
            libraries=libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )
        accession_table["df"].to_csv(
            f"{output}/fetchNGS_input_table.tsv", sep="\t", header=False, index=False
        )

    if ameta == True:
        logger.info("Preparing aMeta table")
        aMeta_table = prepare_aMeta_table(
            samples=samples,
            libraries=libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )
        aMeta_table.to_csv(f"{output}/aMeta_input_table.tsv", sep="\t", index=False)

    logger.info("Preparing Bibtex citation file")
    with open("AncientMetagenomeDir_citations.bib", "w") as fw:
        fw.write(prepare_bibtex_file(samples))

    with open(f"{output}/ancientMetagenomeDir_curl_download_script.sh", "w") as fw:
        fw.write(accession_table["curl_script"])

    with open(f"{output}/ancientMetagenomeDir_aspera_download_script.sh", "w") as fw:
        fw.write(accession_table["aspera_script"])
