import os
from AMDirT.validate.application import AMDirValidator
from AMDirT.autofill.diff import get_sample_diff


def test_get_sample_diff(test_data_dir):
    remote_dataset = os.path.join(test_data_dir, "valid.tsv")
    local_dataset = os.path.join(test_data_dir, "valid_new_rows.tsv")
    schema = os.path.join(test_data_dir, "schema.json")

    local_validator = AMDirValidator(
        schema=schema,
        dataset=local_dataset,
    )
    remote_validator = AMDirValidator(
        schema=schema,
        dataset=remote_dataset,
    )

    diff = diff = get_sample_diff(
        local=local_validator.dataset,
        remote=remote_validator.dataset,
        schema=local_validator.schema,
    )

    assert set(diff) == set(tuple(["ERS2985749", "ERS2985799", "ERS3881517"]))
