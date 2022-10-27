import os
from AMDirT.validate import AMDirValidator


def test_project_multiple_doi(test_data_dir):
    valid_dataset = os.path.join(test_data_dir, "valid.tsv")
    invalid_doi = os.path.join(test_data_dir, "invalid_project_multiple_DOI.tsv")
    schema = os.path.join(test_data_dir, "schema.json")

    valid = AMDirValidator(schema=schema, dataset=valid_dataset)
    invalid = AMDirValidator(schema=schema, dataset=invalid_doi)

    assert valid.check_duplicate_dois() is True

    assert invalid.check_duplicate_dois() is False
