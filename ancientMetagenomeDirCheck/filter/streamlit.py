import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import argparse
import sys
import json
import os
from ancientMetagenomeDirCheck.filter.utils import (
    prepare_eager_table,
    prepare_accession_table,
)


def parse_args():
    parser = argparse.ArgumentParser("Run Streamlit app")
    parser.add_argument("-c", "--config", help="config file", required=True)
    try:
        args = parser.parse_args()
    except SystemExit as e:
        os._exit(e.code)
    return args


args = parse_args()


st.image(
    "https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/master/assets/images/spaam-AncientMetagenomeDir_socialmedia.png"
)
st.markdown("# AncientMetagenomeDir filtering tool")

with open(args.config) as c:
    tables = json.load(c)
    samples = tables["samples"]
    libraries = tables["libraries"]

# Sidebar
with st.sidebar:
    st.write("## Select a table")
    options = ["No table selected"] + list(samples.keys())
    table_name = st.selectbox(label="", options=options)

if table_name != "No table selected":
    # Main content
    st.write(f"Displayed table: {table_name}")
    df = pd.read_csv(
        samples[table_name],
        sep="\t",
    )
    library = pd.read_csv(
        libraries[table_name],
        sep="\t",
    )

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True
    )
    gridOptions = gb.build()

    df_mod = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode="filtered",
        update_mode="filtering_changed",
    )

    stacked_samples = (
        df_mod["data"]["archive_accession"]
        .str.split(",", expand=True)
        .stack()
        .reset_index(level=0)
        .set_index("level_0")
        .rename(columns={0: "archive_accession"})
        .join(df_mod["data"].drop("archive_accession", axis=1))
    )

    library_selected = library.merge(
        stacked_samples[["archive_accession", "sample_host"]],
        left_on="archive_sample_accession",
        right_on="archive_accession",
    )

    # st.write(library_selected)

    if st.button("Give me my data"):
        eager_table = prepare_eager_table(df_mod["data"], library)
        accession_table = prepare_accession_table(df_mod["data"], library)

        st.write("## Eager Table")
        st.write(eager_table)

        st.download_button(
            label="Download Eager table CSV",
            data=eager_table.to_csv(sep="\t").encode("utf-8"),
            file_name="ancientMetagenomeDir_eager_input.csv",
        )

        st.download_button(
            label="Download accesion table TSV",
            data=accession_table.to_csv(sep="\t").encode("utf-8"),
            file_name="ancientMetagenomeDir_accession_table.csv",
        )
