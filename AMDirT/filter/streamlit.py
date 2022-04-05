from numpy import ALLOW_THREADS
import streamlit as st
import pandas as pd

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import argparse
import sys
import json
import os
from AMDirT.core.utils import (
    prepare_eager_table,
    prepare_accession_table,
    is_merge_size_zero,
)

st.set_page_config(
    page_title="AMDirT Filter",
    page_icon="https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/dev/assets/images/spaam-AncientMetagenomeDir_logo_mini.png",
    layout="wide",
)

supported_archives = ["ENA", "SRA"]

if "compute" not in st.session_state:
    st.session_state.compute = False
if "force_validation" not in st.session_state:
    st.session_state.force_validation = False
if "table_name" not in st.session_state:
    st.session_state.table_name = None


def parse_args():
    parser = argparse.ArgumentParser("Run Streamlit app")
    parser.add_argument("-c", "--config", help="json config file", required=True)
    try:
        args = parser.parse_args()
    except SystemExit as e:
        os._exit(e.code)
    return args


args = parse_args()


with open(args.config) as c:
    tables = json.load(c)
    samples = tables["samples"]
    libraries = tables["libraries"]

# Sidebar
with st.sidebar:
    st.markdown(
        """
<p style="text-align:center;"><img src="https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/master/assets/images/spaam-AncientMetagenomeDir_logo_colourmode.svg" alt="logo" width="50%"></p>
""",
        unsafe_allow_html=True,
    )
    st.write("# [AMDirT](https://github.com/SPAAM-community/AMDirT) filtering tool")
    st.write("## Select a table")
    options = ["No table selected"] + list(samples.keys())
    st.session_state.table_name = st.selectbox(label="", options=options)
    st.write(f"Only {' and '.join(supported_archives)} archives are supported for now")

if st.session_state.table_name != "No table selected":
    # Main content
    st.markdown(f"Displayed table: `{st.session_state.table_name}`")
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
        groupable=True,
        value=True,
        enableRowGroup=True,
        aggFunc="sum",
        editable=False,
    )
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()

    with st.form("Samples table") as f:
        st.markdown("Select samples to filter")
        df_mod = AgGrid(
            df,
            gridOptions=gridOptions,
            data_return_mode="filtered",
            update_mode="selection_changed",
        )
        if st.form_submit_button("Validate selection"):
            st.session_state.compute = True

    merge_is_zero = is_merge_size_zero(
        pd.DataFrame(df_mod["selected_rows"]), library, st.session_state.table_name
    )

    if (
        st.session_state.compute
        and not merge_is_zero
        and pd.DataFrame(df_mod["selected_rows"]).shape[0] != 0
    ):
        if pd.DataFrame(df_mod["selected_rows"]).shape[0] == df.shape[0]:
            st.warning(
                "All samples are selected, are you sure you want you want them all ?"
            )
            st.session_state.force_validation = False
            if st.button("Yes"):
                st.session_state.force_validation = True
        else:
            nb_sel_samples = pd.DataFrame(df_mod["selected_rows"]).shape[0]
            st.write(f"{nb_sel_samples } sample{'s'[:nb_sel_samples^1]} selected")
            st.session_state.force_validation = True

        if st.session_state.force_validation:
            st.download_button(
                label="Download Eager TSV table ",
                data=prepare_eager_table(
                    pd.DataFrame(df_mod["selected_rows"]),
                    library,
                    st.session_state.table_name,
                    supported_archives,
                )
                .to_csv(sep="\t", index=False)
                .encode("utf-8"),
                file_name="ancientMetagenomeDir_eager_input.csv",
            )
            st.download_button(
                label="Download accession TSV table for fetchNGS",
                data=prepare_accession_table(
                    pd.DataFrame(df_mod["selected_rows"]),
                    library,
                    st.session_state.table_name,
                    supported_archives,
                )
                .to_csv(sep="\t", header=False, index=False)
                .encode("utf-8"),
                file_name="ancientMetagenomeDir_accession_table.csv",
            )
            if st.button("Reset app"):
                st.session_state.compute = False
                st.session_state.table_name = "No table selected"
                st.session_state.force_validation = False
