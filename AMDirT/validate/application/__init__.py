from typing import Iterable
from AMDirT.validate.domain import DatasetValidator, DFError


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
