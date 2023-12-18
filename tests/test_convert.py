import pytest
from pathlib import Path
import shutil
import os

from AMDirT.convert import run_convert


def test_convert(test_data_dir):
    assert (
        run_convert(
            samples=os.path.join(test_data_dir, "samples_test_convert.tsv"),
            table_name="ancientmetagenome-hostassociated",
            eager=True,
            fetchngs=True,
            ameta=True,
            output="test_files",
        )
        is None
    )
    shutil.rmtree("test_files")
