from sys import path
import os
from AMDirT.core import (
    prepare_accession_table,
    prepare_bibtex_file,
    prepare_eager_table,
    prepare_mag_table,
    prepare_aMeta_table,
    is_merge_size_zero,
    prepare_taxprofiler_table,
    get_libraries,
)
from AMDirT.core import get_json_path
from json import load
from AMDirT.core import logger
import pandas as pd
import warnings


def run_convert(
    samples,
    table_name,
    tables=None,
    output=".",
    bibliography=False,
    librarymetadata=False,
    curl=False,
    aspera=False,
    eager=False,
    fetchngs=False,
    sratoolkit=False,
    ameta=False,
    taxprofiler=False,
    mag=False,
    verbose=False,
):
    """Run the AMDirT conversion application to input samplesheet tables for different pipelines

    Args:
        tables (str): Path to JSON file listing tables
        samples (str): Path to AncientMetagenomeDir filtered samples tsv file
        table_name (str): Name of the table of the table to convert
        output (str): Path to output table. Defaults to "."
    """
    os.makedirs(output, exist_ok=True)

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

    selected_libraries = get_libraries(
        samples=samples,
        libraries=libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )

    accession_table = prepare_accession_table(
        samples=samples,
        libraries=selected_libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )

    logger.warning(
        "We provide no warranty to the accuracy of the generated input sheets."
    )

    if bibliography == True:
        bibfile = f"{output}/AncientMetagenomeDir_bibliography.bib"
        logger.info(f"Writing Bibtex citation file to {bibfile}")
        with open(bibfile, "w") as fw:
            fw.write(prepare_bibtex_file(samples))

    if table_name in ["ancientmetagenome-environmental"]:
        col_drop = ["archive_accession"]
    else:
        col_drop = ["archive_accession", "sample_host"]

    if librarymetadata == True:
        tbl_file = f"{output}/AncientMetagenomeDir_filtered_libraries.tsv"
        logger.info(f"Writing filtered libraries table to {tbl_file}")
        librarymetadata = selected_libraries.drop(col_drop, axis=1)
        librarymetadata.to_csv(
            tbl_file,
            sep="\t",
            index=False,
        )

    if curl == True:
        dl_file = f"{output}/AncientMetagenomeDir_curl_download_script.sh"
        logger.info(f"Writing curl download script to {dl_file}")
        with open(dl_file, "w") as fw:
            fw.write(accession_table["curl_script"])

    if aspera == True:
        dl_file = f"{output}/AncientMetagenomeDir_aspera_download_script.sh"
        logger.info(f"Writing Aspera download script to {dl_file}")
        logger.warning(
            "You will need to set the ${ASPERA_PATH} environment variable. See https://amdirt.readthedocs.io for more information."
        )
        with open(dl_file, "w") as fw:
            fw.write(accession_table["aspera_script"])

    if fetchngs == True:
        dl_file = f"{output}/AncientMetagenomeDir_nf_core_fetchngs_download_script.sh"
        logger.info(f"Writing nf-core/fetchngs table to {dl_file}")
        accession_table["df"]["archive_data_accession"].to_csv(
            dl_file,
            sep="\t",
            header=False,
            index=False,
        )
    if sratoolkit == True:
        dl_file = f"{output}/AncientMetagenomeDir_sratoolkit_download_script.sh"
        logger.info(f"Writing sratoolkit/fasterq-dump download script to {dl_file}")
        with open(dl_file, "w") as fw:
            fw.write(accession_table["fasterq_dump_script"])

    if eager == True:
        tbl_file = f"{output}/AncientMetagenomeDir_nf_core_eager_input_table.tsv"
        logger.info(f"Writing nf-core/eager table to {tbl_file}")
        eager_table = prepare_eager_table(
            samples=samples,
            libraries=selected_libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )
        eager_table.to_csv(
            tbl_file,
            sep="\t",
            index=False,
        )

    if taxprofiler == True:
        tbl_file = f"{output}/AncientMetagenomeDir_nf_core_taxprofiler_input_table.csv"
        logger.info(f"Writing nf-core/taxprofiler table to {tbl_file}")
        taxprofiler_table = prepare_taxprofiler_table(
            samples=samples,
            libraries=selected_libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )
        taxprofiler_table.to_csv(
            tbl_file,
            header=False,
            index=False,
        )

    if ameta == True:
        tbl_file = f"{output}/AncientMetagenomeDir_aMeta_input_table.tsv"
        logger.info(f"Writing aMeta table to {tbl_file}")
        logger.warning(
            "aMeta does not support pairs. You must manually merge pair-end data before using samplesheet."
        )
        aMeta_table = prepare_aMeta_table(
            samples=samples,
            libraries=selected_libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )

        aMeta_table.to_csv(
            tbl_file,
            sep="\t",
            index=False,
        )

    if mag == True:
        logger.info("Preparing nf-core/mag table(s)")
        mag_table_single, mag_table_paired = prepare_mag_table(
            samples=samples,
            libraries=selected_libraries,
            table_name=table_name,
            supported_archives=supported_archives,
        )
        if not mag_table_single.empty:
            mag_tbl_single_file = (
                f"{output}/AncientMetagenomeDir_nf_core_mag_input_single_table.csv"
            )
            logger.info(
                f"Writing nf-core/mag single-end table to {mag_tbl_single_file}"
            )
            mag_table_single.to_csv(
                mag_tbl_single_file,
                index=False,
            )
        if not mag_table_paired.empty:
            mag_tbl_paired_file = (
                f"{output}/AncientMetagenomeDir_nf_core_mag_input_paired_table.csv"
            )
            logger.info(
                f"Writing nf-core/mag paired-end table to {mag_tbl_paired_file}"
            )
            mag_table_paired.to_csv(
                mag_tbl_paired_file,
                index=False,
            )
