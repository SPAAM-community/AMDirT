from sys import path
from AMDirT.core import (
    prepare_accession_table,
    prepare_bibtex_file,
    prepare_eager_table,
    prepare_mag_table,
    is_merge_size_zero,
)
from AMDirT.core import get_json_path
from json import load
from AMDirT.core import logger
import pandas as pd
import warnings


def run_convert(samples, tables, table_name, output=".", verbose=False):
    """Run the AMDirT conversion application to generate Eager and/or fetchNGS tables

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

    logger.info("Preparing Eager table")
    eager_table = prepare_eager_table(
        samples=samples,
        libraries=libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )
    logger.info("Preparing Mag table")
    mag_table_single, mag_table_paired = prepare_mag_table(
        samples=samples,
        libraries=libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )
    logger.info("Preparing Accession table")
    accession_table = prepare_accession_table(
        samples=samples,
        libraries=libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )
    logger.info("Preparing Bibtex citation file")
    with open("AncientMetagenomeDir_citations.bib", "w") as fw:
        fw.write(prepare_bibtex_file(samples))
 

    eager_table.to_csv(
        f"{output}/eager_input_table.tsv", sep="\t", index=False
    )
    if not mag_table_single.empty:
        mag_table_single.to_csv(
            f"{output}/mag_input_single_table.csv", index=False
        )
    if not mag_table_paired.empty:
        mag_table_paired.to_csv(
            f"{output}/mag_input_paired_table.csv", index=False
        )
    accession_table["df"].to_csv(
        f"{output}/fetchNGS_input_table.tsv", sep="\t", header=False, index=False
    )
    with open("ancientMetagenomeDir_curl_download_script.sh", "w") as fw:
        fw.write(accession_table["script"])
