from AMDirT.validate.domain import DatasetValidator, DFError


class AMDirValidator(DatasetValidator):
    def check_duplicate_dois(self):
        project_dois = self.dataset.groupby("project_name")["publication_doi"].unique()
        doi_unique = self.dataset.groupby("project_name")["publication_doi"].nunique()
        for project in doi_unique.index:
            if doi_unique[project] > 1:
                self.add_error(
                    DFError(
                        error="Duplicated DOI Error",
                        source=project_dois[project],
                        column="publication_doi",
                        row=None,
                        message=f"Duplicate DOI for {project} project. Make sure each project has a single DOI",
                    )
                )


if __name__ == "__main__":

    s = "/Users/maxime/Documents/github/AMDirT/test/data/schema.json"
    d = "/Users/maxime/Documents/github/AMDirT/test/data/invalid.tsv"

    v = AMDirValidator(s, d)
    v.check_duplicate_dois()
    print(v.to_rich())
