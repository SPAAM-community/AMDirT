import os
from AMDirT.autofill.diff import get_sample_diff


def test_get_sample_diff(test_data_dir):
    remote_dataset = os.path.join(test_data_dir, "valid.tsv")
    local_dataset = os.path.join(test_data_dir, "valid_new_rows.tsv")
    schema = os.path.join(test_data_dir, "schema.json")

    diff = get_sample_diff(local=local_dataset, remote=remote_dataset, schema=schema)

    assert set(diff) == set(tuple(["ERS2985749", "ERS2985799", "ERS3881517"]))
