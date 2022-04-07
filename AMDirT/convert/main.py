from sys import path
from AMDirT.core.utils import (
    prepare_accession_table,
    prepare_eager_table,
    is_merge_size_zero,
)
from AMDirT.filter.run_streamlit import get_json_path
from json import load
import logging
import pandas as pd


def run_convert(samples, table_name, tables, output):
    supported_archives = ["ENA", "SRA"]
    if tables is None:
        table_path = get_json_path()
        with open(table_path, "r") as f:
            tables = load(f)
    table_list = list(tables["samples"].keys())
    if table_name not in table_list:
        logging.info(f"Table '{table_name}' not found in {table_list}")

    #fixme
    libraries = pd.read_csv(tables["libraries"][table_name], sep="\t")

    eager_table = prepare_eager_table(
        samples=samples,
        libraries=libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )

    accession_table = prepare_accession_table(
        samples=samples,
        libraries=libraries,
        table_name=table_name,
        supported_archives=supported_archives,
    )

    eager_table.to_csv(f"{output}/eager_input_table.tsv", sep="\t", index=False)
    accession_table.to_csv(
        f"{output}/fetchNGS_input_table.tsv", sep="\t", header=False, index=False
    )
