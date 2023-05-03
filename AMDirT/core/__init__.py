from typing import Tuple, Iterable
from pathlib import Path
import requests
from numpy import where
import pandas as pd
import streamlit as st
from packaging import version
from importlib.resources import files as get_module_dir
import os
import logging
import colorlog

pd.options.mode.chained_assignment = None


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
	'%(log_color)s%(name)s [%(levelname)s]: %(message)s'))

logger = colorlog.getLogger('AMDirT')
logger.addHandler(handler)
logger.propagate = False


def get_json_path():
    path = get_module_dir("AMDirT.assets").joinpath("tables.json")
    return path


@st.cache_data
def get_amdir_tags():
    r = requests.get(
        "https://api.github.com/repos/SPAAM-community/AncientMetagenomeDir/tags"
    )
    if r.status_code == 200:
        return [
            tag["name"]
            for tag in r.json()
            if version.parse(tag["name"]) >= version.parse("v22.09")
        ]
    else:
        return []


def get_colour_chemistry(instrument: str) -> int:
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


def doi2bib(doi: str) -> str:
    """
    Return a bibTeX string of metadata for a given DOI.
    """

    url = "http://doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)

    return r.text

@st.cache_data
def get_libraries(table_name: str, samples: pd.DataFrame, libraries: pd.DataFrame, supported_archives: Iterable[str]):
    """Get filtered libraries from samples and libraries tables

    Args:
        table_name (str): Name of the table of the table to convert
        samples (pd.DataFrame): Sample table
        libraries (pd.DataFrame): Library table
        supported_archives (Iterable[str]): Supported archives list

    Returns:
        pd.DataFrame: filtered libraries table
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

    return selected_libraries

def get_filename(path_string: str, orientation: str) -> Tuple[str, str]:
    """
    Get Fastq Filename from download_links column

    Args:
        path_string(str): path to fastq files urls, comma separated
        orientation(str): [fwd | rev]
    Returns
        str: name of Fastq file
    """

    if ";" in path_string:
        fwd = Path(path_string.split(";")[0]).name
        rev = Path(path_string.split(";")[1]).name
    else:
        fwd = Path(path_string).name
        rev = "NA"
    if orientation == "fwd":
        return fwd
    elif orientation == "rev":
        return rev

def parse_to_mag(selected_libraries):

    selected_libraries["short_reads_1"] = selected_libraries["download_links"].apply(
        get_filename, orientation="fwd"
    )
    selected_libraries["short_reads_2"] = selected_libraries["download_links"].apply(
        get_filename, orientation="rev"
    )
    selected_libraries["short_reads_2"] = selected_libraries["short_reads_2"].replace(
        "NA", ""
    )
    selected_libraries["longs_reads"] = ""
    col2keep = [
        "archive_data_accession",
        "archive_sample_accession",
        "short_reads_1",
        "short_reads_2",
        "longs_reads",
    ]
    selected_libraries = selected_libraries[col2keep].rename(
        columns={
            "archive_data_accession": "sample",
            "archive_sample_accession": "group",
        }
    )
    return selected_libraries

@st.cache_data
def prepare_eager_table(
    samples: pd.DataFrame,
    libraries: pd.DataFrame,
    table_name: str,
    supported_archives: Iterable[str],
) -> pd.DataFrame:
    """Prepare nf-core/eager tsv input table

    Args:
        sample (pd.dataFrame): selected samples table
        library (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """
    selected_libraries = get_libraries(
        table_name=table_name,
        samples=samples,
        libraries=libraries,
        supported_archives=supported_archives,
    )

    selected_libraries["Colour_Chemistry"] = selected_libraries[
        "instrument_model"
    ].apply(get_colour_chemistry)

    selected_libraries[
        "UDG_Treatment"
    ] = selected_libraries.library_treatment.str.split("-", expand=True)[0]

    selected_libraries["R1"] = selected_libraries["download_links"].apply(
        get_filename, orientation="fwd"
    )

    selected_libraries["R2"] = selected_libraries["download_links"].apply(
        get_filename, orientation="rev"
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


@st.cache_data
def prepare_mag_table(
    samples: pd.DataFrame,
    libraries: pd.DataFrame,
    table_name: str,
    supported_archives: Iterable[str],
) -> pd.DataFrame:
    """Prepare nf-core/mag tsv input table

    Args:
        sample (pd.dataFrame): selected samples table
        library (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """

    selected_libraries = get_libraries(
        table_name=table_name,
        samples=samples,
        libraries=libraries,
        supported_archives=supported_archives,
    )

    # Create a DataFrame for "SINGLE" values
    single_libraries = selected_libraries[selected_libraries["library_layout"] == "SINGLE"]

    # Create a DataFrame for "PAIRED" values
    paired_libraries = selected_libraries[selected_libraries["library_layout"] == "PAIRED"]

    if not single_libraries.empty:
        single_libraries = parse_to_mag(single_libraries)
    if not paired_libraries.empty:
        paired_libraries = parse_to_mag(paired_libraries)

    return single_libraries, paired_libraries

@st.cache_data
def prepare_accession_table(
    samples: pd.DataFrame,
    libraries: pd.DataFrame,
    table_name: str,
    supported_archives: Iterable[str],
) -> pd.DataFrame:
    """Get accession lists for samples and libraries

    Args:
        samples (pd.dataFrame): selected samples table
        libraries (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """

    selected_libraries = get_libraries(
        table_name=table_name,
        samples=samples,
        libraries=libraries,
        supported_archives=supported_archives,
    )

    # Downloading with curl or aspera instead of fetchngs
    urls = set(selected_libraries["download_links"])
    links = set()
    for u in urls:
        for s in u.split(";"):
            links.add(s)
    dl_script_header = "#!/usr/bin/env bash\n"
    curl_script = (
        "\n".join([f"curl -L ftp://{l} -o {l.split('/')[-1]}" for l in links]) + "\n"
    )
    aspera_script = (
        "\n".join(
            [
                "ascp -QT -l 300m -P 33001 "
                "-i ${ASPERA_PATH}/etc/asperaweb_id_dsa.openssh "
                f"era-fasp@fasp.sra.ebi.ac.uk:{'/'.join(l.split('/')[1:])} ."
                for l in links
            ]
        )
        + "\n"
    )

    return {
        "df": selected_libraries[
            ["archive_accession", "download_sizes"]
        ].drop_duplicates(),
        "curl_script": dl_script_header + curl_script,
        "aspera_script": dl_script_header + aspera_script,
    }

@st.cache_data
def prepare_taxprofiler_table(
    samples: pd.DataFrame,
    libraries: pd.DataFrame,
    table_name: str,
    supported_archives: Iterable[str],
) -> pd.DataFrame:
    """Prepare taxprofiler csv input table

    Args:
        sample (pd.dataFrame): selected samples table
        library (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """
    selected_libraries = get_libraries(
        table_name=table_name,
        samples=samples,
        libraries=libraries,
        supported_archives=supported_archives,
    )

    selected_libraries["fastq_1"] = selected_libraries["download_links"].apply(
        get_filename, orientation="fwd"
    )

    selected_libraries["fastq_2"] = selected_libraries["download_links"].apply(
        get_filename, orientation="rev"
    )

    selected_libraries["fastq_2"] = selected_libraries["fastq_2"].replace(
        "NA", ""
    )

    selected_libraries["fasta"] = ""

    selected_libraries['instrument_model'] = where(selected_libraries['instrument_model'].str.lower().str.contains('illumina|nextseq|hiseq|miseq'), 'ILLUMINA',
        where(selected_libraries['instrument_model'].str.lower().str.contains('torrent'), 'ION_TORRENT',
        where(selected_libraries['instrument_model'].str.lower().str.contains('helicos'), 'HELICOS',
        where(selected_libraries['instrument_model'].str.lower().str.contains('bgiseq'), 'BGISEQ',
        where(selected_libraries['instrument_model'].str.lower().str.contains('454'), 'LS454',
        selected_libraries['instrument_model']))))
    )

    col2keep = ["sample_name", "library_name", "instrument_model", "fastq_1", "fastq_2", "fasta"]
    selected_libraries = selected_libraries[col2keep].rename(
        columns={
            "sample_name": "sample",
            "library_name": "run_accession",
            "instrument_model": "instrument_platform"
        }
    )

    return selected_libraries


@st.cache_data
def prepare_aMeta_table(
    samples: pd.DataFrame,
    libraries: pd.DataFrame,
    table_name: str,
    supported_archives: Iterable[str],
) -> pd.DataFrame:
    """Prepare aMeta tsv input table

    Args:
        sample (pd.dataFrame): selected samples table
        library (pd.dataFrame): library table
        table_name (str): Name of the table
        supported_archives (list): list of supported archives
    """
    selected_libraries = get_libraries(
        table_name=table_name,
        samples=samples,
        libraries=libraries,
        supported_archives=supported_archives,
    )

    selected_libraries["Colour_Chemistry"] = selected_libraries[
        "instrument_model"
    ].apply(get_colour_chemistry)

    selected_libraries[
        "UDG_Treatment"
    ] = selected_libraries.library_treatment.str.split("-", expand=True)[0]

    selected_libraries["R1"] = selected_libraries["download_links"].apply(
        get_filename, orientation="fwd"
    )

    selected_libraries["R2"] = selected_libraries["download_links"].apply(
        get_filename, orientation="rev"
    )

    selected_libraries["Lane"] = 0
    selected_libraries["SeqType"] = where(
        selected_libraries["library_layout"] == "SINGLE", "SE", "PE"
    )
    selected_libraries["BAM"] = "NA"
    if table_name == "ancientmetagenome-environmental":
        selected_libraries["sample_host"] = "environmental"
    col2keep = ["archive_data_accession", "R1"]
    selected_libraries = selected_libraries[col2keep].rename(
        columns={
            "archive_data_accession": "sample",
            "R1": "fastq",
        }
    )

    return selected_libraries


@st.cache_data
def prepare_bibtex_file(samples: pd.DataFrame) -> str:
    dois = set()
    failed_dois = set()
    dois_set = set(list(samples["publication_doi"]))
    dois_set.add("10.1038/s41597-021-00816-y")
    for doi in dois_set:
        try:
            bibtex_str = doi2bib(doi)
            if len(bibtex_str) == 0:
                failed_dois.add(doi)
            else:
                dois.add(bibtex_str)
        except Exception as e:
            logger.info(e)
            pass
    # Print warning for DOIs that do not have an entry
    if len(failed_dois) > 0:
        st.warning(
            "Citation information could not be resolved for the "
            "following DOIs: " + ", ".join(failed_dois) + ". Please "
            "check how to cite these publications manually!"
        )
        logger.warning(
            "Citation information could not be resolved for the "
            "following DOIs: " + ", ".join(failed_dois) + ". Please "
            "check how to cite these publications manually!"
        )

    dois_string = "\n".join(list(dois))
    return dois_string


def is_merge_size_zero(
    samples: pd.DataFrame, library: pd.DataFrame, table_name: str
) -> bool:
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
