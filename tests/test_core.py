import pytest

from AMDirT.core.utils import (
    get_colour_chemistry,
    get_experiment_accession,
    get_study_table,
    doi2bib,
    get_filename,
)


def test_get_colour_chemistry():

    assert get_colour_chemistry("hiseq") == 4
    assert get_colour_chemistry("novaseq") == 2


def test_get_experiment_accession():

    assert get_experiment_accession("SRR957738") == "SRX340010"

    with pytest.raises(KeyError) as error_info:
        get_experiment_accession("SRS7890496")


def test_get_study_table():
    assert get_study_table("PRJNA216965").iloc[0, :]["run_accession"] == "SRR957738"


def test_doi2bib():
    assert doi2bib("10.1038/nature14236")[:18] == "@article{Mnih_2015"
