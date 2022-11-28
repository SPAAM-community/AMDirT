from typing import Iterable, AnyStr, Union
from AMDirT.validate.domain import DatasetValidator, DFError
from AMDirT.core import get_json_path
from AMDirT.core.diff import get_sample_diff
from AMDirT.core.ena import ENAPortalAPI
from pathlib import Path
import json


class AMDirValidator(DatasetValidator):
    """Validator Class for AncientMetagenomeDir datasets"""

    def check_duplicate_dois(self) -> bool:
        project_dois = self.dataset.groupby("project_name")[
            "data_publication_doi"
        ].unique()
        doi_unique = self.dataset.groupby("project_name")[
            "data_publication_doi"
        ].nunique()
        err_cnt = 0
        for project in doi_unique.index:
            if doi_unique[project] > 1:
                err_cnt += 1
                self.add_error(
                    DFError(
                        error="Duplicated DOI Error",
                        source=project_dois[project],
                        column="data_publication_doi",
                        row="",
                        message=f"Duplicate DOI for {project} project. Make sure each project has a single DOI",
                    )
                )
        if err_cnt > 0:
            return False
        return True

    def check_multi_values(
        self, column_names: Iterable[str] = ["archive_accession"]
    ) -> bool:
        """Check for duplicates entries in multi values column
        Args:
            column_names (Iterable[str], optional): List of multi values columns to check for duplications. Defaults to ["archive_accession"].
        """
        err_cnt = 0
        for column in column_names:
            row = 0
            for archives in self.dataset[column]:
                archives = archives.split(",")
                if len(set(archives)) != len(archives):
                    self.add_error(
                        DFError(
                            error="Duplicates in multi values column",
                            source=archives,
                            column=column,
                            row=row + 2,
                            message=f"Duplicates in multi values column {column}. Make sure each value in combination is unique",
                        )
                    )
                    err_cnt += 1
                row += 1
        if err_cnt > 0:
            return False
        else:
            return True

    def check_sample_accession(self, remote: Union[AnyStr, None] = None) -> bool:
        """Check that sample accession are valid

        Args:
            remote (AnyStr | None, optional): Remote to check against. Defaults to None.
        """

        if not remote:
            with open(get_json_path()) as f:
                tables = json.load(f)
            samples = tables["samples"]
            for table in samples:
                if self.dataset_name == Path(samples[table]).name:
                    remote = samples[table]
            if remote is None:
                raise SystemExit(
                    f"No remote found for {self.dataset} dataset, please provide one"
                )
        remote_samples = DatasetValidator(schema=self.schema_path, dataset=remote)
        new_samples = get_sample_diff(
            local=self.dataset, remote=remote_samples.dataset, schema=self.schema
        )
        df_change = self.dataset[
            self.dataset["archive_accession"].str.contains("|".join(new_samples))
        ]
        if len(new_samples) > 0:
            e = ENAPortalAPI()
            change_dict = {}
            for i in df_change.index:
                if df_change.loc[i, "archive"] in ["SRA", "ENA"]:
                    samples = df_change.loc[i, "archive_accession"].split(",")
                    project = df_change.loc[i, "archive_project"]
                    if project not in change_dict:
                        change_dict[project] = {"index": i, "sample": samples}
                    else:
                        change_dict[project]["sample"].extend(samples)
                else:
                    continue
            for project in change_dict:
                json_result = e.query(
                    accession=project,
                    result_type="read_experiment",
                    fields=["secondary_sample_accession"],
                )
                ena_samples = []
                for i in json_result:
                    ena_samples.append(i["secondary_sample_accession"])
                for sample in change_dict[project]["sample"]:
                    if sample not in ena_samples:
                        self.add_error(
                            DFError(
                                error="Invalid sample accession",
                                source=sample,
                                column="archive_accession",
                                row=change_dict[project]["index"] + 2,
                                message=f"Sample accession {sample} is not valid",
                            )
                        )
                        return False
                return True
