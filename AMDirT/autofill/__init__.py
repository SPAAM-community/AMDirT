from AMDirT.validate.domain import DatasetValidator
from AMDirT.core import get_json_path, logger
from AMDirT.core.ena import ENAPortalAPI
import json

import sys
import pandas as pd

def run_autofill(accession, accession_type, table_name=None, schema=None, dataset=None, output=None, verbose=False):
    """Autofill the metadata of a table from ENA

    Args:
        accession (str): ENA project accession
        accession_type (str): ENA project accession type
        table_name (str): Name of the table to be filled
        schema (str): Path to the schema file
        dataset (str): Path to the dataset file
        output (str): Path to the output table file

    Returns:
        pd.DataFrame: ENA metadata run level table
    """

    if schema is None and dataset is None:
        json_conf = get_json_path()
        with open(json_conf) as c:
            tables = json.load(c)
            samples = tables["samples"]
            samples_schema = tables["samples_schema"]
            libraries = tables["libraries"]
            libraries_schema = tables["libraries_schema"]
        if table_name not in samples:
            raise Exception("Table name not found in AncientMetagenomeDir file")
    else:
        logger.error("Not implemented yet")


    

    sample = DatasetValidator(
        schema=samples_schema[table_name], dataset=samples[table_name]
    )
    libraries = DatasetValidator(
        schema=libraries_schema[table_name], dataset=libraries[table_name]
    )

    libraries.to_rich()

    sample_df = sample.dataset.iloc[:0, :].copy()
    libraries_df = libraries.dataset.iloc[:0, :].copy()

    ena = ENAPortalAPI()
    if ena.status():
        logger.info("ENA API is up")
    else:
        logger.error("ENA API is down")
        sys.exit(1)
    query_res = ena.query(accession, fields=[
        "study_accession",
        "run_accession",
        "sample_accession",
        "sample_alias",
        "fastq_ftp",
        "fastq_md5",
        "fastq_bytes",
        "library_name",
        "instrument_model",
        "library_layout",
        "library_strategy",
        "read_count",
    ])
    res = pd.DataFrame.from_dict(query_res)
    if accession_type == "project":
        res['archive_project'] = accession
    elif accession_type == "sample":
        res["archive_sample_accession"] = accession
    else:
        logger.error("Accession type not recognized")
        sys.exit(1)
    res.rename(
        columns={
            "study_accession": "archive_project",
            "run_accession":"archive_data_accession",
            "sample_accession": "archive_sample_accession",
            "sample_alias": "sample_name",
            "fastq_ftp": "download_links",
            "fastq_md5": "download_md5s",
            "fastq_bytes": "download_sizes"
        },
        inplace=True
        )
    for col in libraries_df.columns:
        if col not in res.columns:
            res[col] = None
    res = res[libraries_df.columns]
    res = res.loc[:,~res.columns.duplicated()].copy()
    logger.info(f"Found {res.shape[0]} libraries")
    logger.info(f"Writing libraries metadata to {output}")
    res.to_csv(output, index=False, sep="\t")
