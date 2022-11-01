import requests
import logging
import os
from typing import List, Dict


class ENA:
    """Abstract class for querying the ENA API"""

    def __init__(self) -> None:
        self.base_url = "https://www.ebi.ac.uk/ena"

    def __repr__(self) -> str:
        """Display URL of API documentation"""
        return f"The documentation for the {self.__class__.__name__} API can be found at {self.base_url}"

    def status(self) -> bool:
        """Check if API is up

        Returns:
            bool: True if API is up, False otherwise
        """
        try:
            resp = requests.get(self.base_url)
            if resp.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.ConnectionError:
            return False

    def doc(self, dir: str = ".") -> None:
        """Get PDF documentation for API

        Args:
            dir(str): path to output PDF directory
        """
        r = requests.get(self.base_url + "doc")
        pdf = os.path.join(
            os.path.expanduser(dir), f"{self.__class__.__name__}_APIDocumentation.pdf"
        )
        with open(pdf, "wb") as fw:
            fw.write(r.content)
        logging.info(
            f"{self.__class__.__name__} documentation has been written to {pdf}"
        )

    def __get_json__(self, url: str) -> List[Dict]:
        """Get json content from URL

        Args:
            url(str): URL to get json content from
        Returns:
            List[Dict]: json content
        """
        resp = requests.get(url)
        if resp.status_code == 200:
            if len(resp.json()) > 0:
                return resp.json()
            else:
                logging.warning("No results found")
                return []


class ENABrowserAPI(ENA):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://www.ebi.ac.uk/ena/browser/api/"


class ENAPortalAPI(ENA):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://www.ebi.ac.uk/ena/portal/api/"

    def get_study_runs(self, study_accession: str) -> dict:
        """Generate list of runs for a given study accession

        Args:
            study_accession (str): study accession

        Returns:
            dict: run_accession as keys, and metadata as values
        """
        url = os.path.join(
            self.base_url,
            f"filereport?accession={study_accession}&download=false&format=json&result=read_run",
        )
        json_resp = self.__get_json__(url)
        d = dict()
        for run in json_resp:
            if "run_accession" in run:
                run_tmp = run.copy()
                run_tmp.pop("run_accession")
                d[run["run_accession"]] = run_tmp
        return d


if __name__ == "__main__":
    e = ENAPortalAPI()
    print(e.get_study_runs("PRJEB30331"))
