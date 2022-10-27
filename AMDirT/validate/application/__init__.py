from AMDirT.validate.domain import DatasetValidator, DFError
from AMDirT import logger


class AMDirValidator(DatasetValidator):
    def check_duplicate_dois(self):
        project_dois = self.dataset.groupby("project_name")["publication_doi"].unique()
        doi_unique = self.dataset.groupby("project_name")["publication_doi"].nunique()
        err_cnt = 0
        for project in doi_unique.index:
            if doi_unique[project] > 1:
                err_cnt += 1
                self.add_error(
                    DFError(
                        error="Duplicated DOI Error",
                        source=project_dois[project],
                        column="publication_doi",
                        row=None,
                        message=f"Duplicate DOI for {project} project. Make sure each project has a single DOI",
                    )
                )
        if err_cnt > 0:
            return False
        return True

    def check_duplicates_archive_accession(self):
        """Check for duplicates entries in archive_accession column
        """
        logger.info('Not yet implemented')

    
