import imp
from os import path
import requests
import xmltodict
from numpy import where
import pandas as pd
import streamlit as st
import pkg_resources
from AMDirT import logger

pd.options.mode.chained_assignment = None


def get_json_path(rel_path="../assets/tables.json"):
    path = pkg_resources.resource_filename(__name__, rel_path)
    return path


def get_colour_chemistry(instrument):
    """
    Get number of colours used in sequencing chemistry
    Args:
        instrument(str): Name of the instrument
    Returns:
        int: number of colours used in sequencing chemistry
    """
    chemistry_colours = {
        "bgiseq": 4,
        "miseq": 4,
        "hiseq": 4,
        "genome analyzer": 4,
        "nextseq": 2,
        "novaseq": 2,
    }

    for k in chemistry_colours:
        if k in instrument.lower():
            return chemistry_colours[k]


def get_experiment_accession(run_accession):
    resp = requests.get(f"https://www.ebi.ac.uk/ena/browser/api/xml/{run_accession}")
    tree = xmltodict.parse(resp.content.decode())
    return tree["RUN_SET"]["RUN"]["EXPERIMENT_REF"]["@accession"]


def get_study_table(study_accession):
    url = (
        "https://www.ebi.ac.uk/ena/portal/api/filereport"
        f"?accession={study_accession}&result=read_run&fields="
        "run_accession,"
        "scientific_name,"
        "library_layout,"
        "library_strategy,"
        "instrument_platform,"
        "submitted_ftp,"
        "submitted_md5,"
        "submitted_bytes,"
        "submitted_format,"
        "fastq_ftp"
    )
    print(url)
    return pd.read_csv(url, sep="\t")


def doi2bib(doi):
    """
    Return a bibTeX string of metadata for a given DOI.
    """

    url = "http://doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)

    return r.text


def get_filename(path_string, prepend_exp=False):
    """
    Get Fastq Filename from download_links column

    Args:
        path_string(str): path to fastq files urls, comma separated
        orientation(str): [fwd | rev]
        prepend_exp(bool): prepend experiment accession number
    Returns
        str: name of Fastq file
    """

    try:
        path_string = str(path_string)
        if path_string == "nan":
            return "NA"
        fwd, rev = path_string.split(";")
        fwd = fwd.split("/")[-1]
        rev = rev.split("/")[-1]
    except (ValueError, AttributeError):
        fwd = path_string
        fwd = fwd.split("/")[-1]
    if prepend_exp:
        run_accession = fwd.split(".")[0].split("_")[0]
        exp_accession = get_experiment_accession(run_accession)
    try:
        if prepend_exp:
            fwd = f"{exp_accession}_{fwd}"
            rev = f"{exp_accession}_{rev}"
        return fwd, rev
    except UnboundLocalError:
        return fwd, "NA"


@st.cache()
def prepare_eager_table(samples, libraries, table_name, supported_archives):
    """Prepare nf-core/eager tsv input table

    Args:
        sample (pd.dataFrame): selected samples table
        library (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """
    stacked_samples = (
        samples.query("archive in @supported_archives")
        .loc[:, "archive_accession"]
        .str.split(",", expand=True)
        .stack()
        .reset_index(level=0)
        .set_index("level_0")
        .rename(columns={0: "archive_accession"})
        .join(samples.drop("archive_accession", axis=1))
    )

    if table_name in [
        "ancientmetagenome-environmental",
    ]:
        sel_col = ["archive_accession"]
    else:
        sel_col = ["archive_accession", "sample_host"]
    libraries = libraries.merge(
        stacked_samples[sel_col],
        left_on="archive_sample_accession",
        right_on="archive_accession",
    )
    select_libs = list(stacked_samples["archive_accession"])
    selected_libraries = libraries.query("archive_sample_accession in @select_libs")

    selected_libraries["Colour_Chemistry"] = selected_libraries[
        "instrument_model"
    ].apply(get_colour_chemistry)

    selected_libraries[
        "UDG_Treatment"
    ] = selected_libraries.library_treatment.str.split("-", expand=True)[0]

    selected_libraries["download_links"].apply(get_filename, prepend_exp=True)

    selected_libraries["R1"], selected_libraries["R2"] = zip(
        *selected_libraries["download_links"].apply(get_filename, prepend_exp=True)
    )
    selected_libraries["Lane"] = 0
    selected_libraries["SeqType"] = where(
        selected_libraries["library_layout"] == "SINGLE", "SE", "PE"
    )
    selected_libraries["BAM"] = "NA"
    if table_name == "ancientmetagenome-environmental":
        selected_libraries["sample_host"] = "environmental"
    col2keep = [
        "sample_name",
        "archive_data_accession",
        "Lane",
        "Colour_Chemistry",
        "SeqType",
        "sample_host",
        "strand_type",
        "UDG_Treatment",
        "R1",
        "R2",
        "BAM",
    ]
    selected_libraries = selected_libraries[col2keep].rename(
        columns={
            "sample_name": "Sample_Name",
            "archive_data_accession": "Library_ID",
            "sample_host": "Organism",
            "strand_type": "Strandedness",
        }
    )

    return selected_libraries


@st.cache()
def prepare_accession_table(samples, libraries, table_name, supported_archives):
    """Get accession lists for samples and libraries

    Args:
        samples (pd.dataFrame): selected samples table
        libraries (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """

    stacked_samples = (
        samples.query("archive in @supported_archives")
        .loc[:, "archive_accession"]
        .str.split(",", expand=True)
        .stack()
        .reset_index(level=0)
        .set_index("level_0")
        .rename(columns={0: "archive_accession"})
        .join(samples.drop("archive_accession", axis=1))
    )
    if table_name in [
        "ancientmetagenome-environmental",
    ]:
        sel_col = ["archive_accession"]
    else:
        sel_col = ["archive_accession", "sample_host"]
    libraries = libraries.merge(
        stacked_samples[sel_col],
        left_on="archive_sample_accession",
        right_on="archive_accession",
    )
    select_libs = list(stacked_samples["archive_accession"])
    selected_libraries = libraries.query("archive_sample_accession in @select_libs")

    # Downloading with curl instead of fetchngs
    urls = set(selected_libraries["download_links"])
    links = set()
    for u in urls:
        for s in u.split(";"):
            links.add(s)
    dl_script = "#!/usr/bin/env bash\n"
    for l in links:
        dl_script += f"curl -L ftp://{l} -o {l.split('/')[-1]}\n"

    return {
        "df": selected_libraries["archive_accession"].to_frame().drop_duplicates(),
        "script": dl_script,
    }


@st.cache()
def prepare_bibtex_file(samples):
    dois = set()
    dois_set = set(list(samples["publication_doi"]))
    dois_set.add("10.1038/s41597-021-00816-y")
    for doi in dois_set:
        try:
            dois.add(doi2bib(doi))
        except Exception as e:
            logger.info(e)
            pass

    dois_string = "\n".join(list(dois))
    return dois_string


def is_merge_size_zero(samples, library, table_name):
    """
    Checks if intersection of samples and libraries table is not null

    Args:
        samples(pd.dataFrame): selected samples table
        libraries (pd.dataFrame): library table
        table_name (str): Name of the table
    """

    if samples.shape[0] == 0 or library.shape[0] == 0:
        return True
    stacked_samples = (
        samples["archive_accession"]
        .str.split(",", expand=True)
        .stack()
        .reset_index(level=0)
        .set_index("level_0")
        .rename(columns={0: "archive_accession"})
        .join(samples.drop("archive_accession", axis=1))
    )

    if table_name in [
        "ancientmetagenome-environmental",
    ]:
        sel_col = ["archive_accession"]
    else:
        sel_col = ["archive_accession", "sample_host"]
    library_selected = library.merge(
        stacked_samples[sel_col],
        left_on="archive_sample_accession",
        right_on="archive_accession",
    )

    if samples.shape[0] != 0 and library_selected.shape[0] == 0:
        return True
    return False