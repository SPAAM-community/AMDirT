from numpy import ALLOW_THREADS
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
    is_merge_size_zero,
)

if "compute" not in st.session_state:
    st.session_state.compute = False
if "table_name" not in st.session_state:
    st.session_state.table_name = None
if "filtered" not in st.session_state:
    st.session_state.filtered = False


def parse_args():
    parser = argparse.ArgumentParser("Run Streamlit app")
    parser.add_argument("-c", "--config", help="config file", required=True)
    try:
        args = parser.parse_args()
    except SystemExit as e:
        os._exit(e.code)
    return args


args = parse_args()


st.markdown(
    """
<p style="text-align:center;"><img src="https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/master/assets/images/spaam-AncientMetagenomeDir_socialmedia.png" alt="logo" width="200"></p>
""",
    unsafe_allow_html=True,
)

with open(args.config) as c:
    tables = json.load(c)
    samples = tables["samples"]
    libraries = tables["libraries"]

# Sidebar
with st.sidebar:
    st.write("# AncientMetagenomeDir filtering tool")
    st.write("## Select a table")
    options = ["No table selected"] + list(samples.keys())
    st.session_state.table_name = st.selectbox(label="", options=options)

if st.session_state.table_name != "No table selected":
    # Main content
    st.write(f"Displayed table: {st.session_state.table_name}")
    df = pd.read_csv(
        samples[st.session_state.table_name],
        sep="\t",
    )
    library = pd.read_csv(
        libraries[st.session_state.table_name],
        sep="\t",
    )

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=False
    )
    gridOptions = gb.build()

    with st.form("Samples table") as f:
        df_mod = AgGrid(
            df,
            gridOptions=gridOptions,
            data_return_mode="filtered",
            update_mode="filtering_changed",
        )
        if st.form_submit_button("Give me my data") or st.session_state.filtered:
            st.session_state.compute = True
            st.session_state.filtered = True

    merge_is_zero = is_merge_size_zero(
        df_mod["data"], library, st.session_state.table_name
    )

    if merge_is_zero:
        st.error("No libraries could be retrieved")
    if df_mod["data"].shape[0] == df.shape[0] and st.session_state.compute:
        st.session_state.filtered = False
        st.markdown("**All samples selected, are you sure to continue?**")
        if st.button("Yes, continue"):
            st.session_state.filtered = True
    if (
        st.session_state.compute
        and st.session_state.filtered
        and not merge_is_zero
        and df_mod["data"].shape[0] != 0
    ):

        st.session_state.filtered = False

        st.download_button(
            label="Download Eager table CSV",
            data=prepare_eager_table(
                df_mod["data"], library, st.session_state.table_name
            )
            .to_csv(sep="\t")
            .encode("utf-8"),
            file_name="ancientMetagenomeDir_eager_input.csv",
        )

        st.download_button(
            label="Download accession table TSV",
            data=prepare_accession_table(
                df_mod["data"], library, st.session_state.table_name
            )
            .to_csv(sep="\t")
            .encode("utf-8"),
            file_name="ancientMetagenomeDir_accession_table.csv",
        )
        if st.button("Reset app"):
            st.session_state.compute = False
            st.session_state.table_name = "No table selected"
