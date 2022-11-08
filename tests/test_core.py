import pytest

from AMDirT.core import (
    get_colour_chemistry,
    get_experiment_accession,
    doi2bib,
    ena,
)


def test_get_colour_chemistry():

    assert get_colour_chemistry("hiseq") == 4
    assert get_colour_chemistry("novaseq") == 2


def test_get_experiment_accession():

    assert get_experiment_accession("SRR957738") == "SRX340010"

    with pytest.raises(KeyError) as error_info:
        get_experiment_accession("SRS7890496")


def test_doi2bib():
    assert doi2bib("10.1038/nature14236")[:18] == "@article{Mnih_2015"


def test_ena_portal_status():
    ena_portal = ena.ENAPortalAPI()
    assert ena_portal.status() is True


def test_ena_browser_status():
    ena_browser = ena.ENABrowserAPI()
    assert ena_browser.status() is True
