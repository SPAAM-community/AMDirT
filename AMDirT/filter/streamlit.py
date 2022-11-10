from numpy import ALLOW_THREADS
import streamlit as st
import pandas as pd

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import argparse
import json
import os
from AMDirT import __version__
from AMDirT.core import (
    prepare_bibtex_file,
    prepare_eager_table,
    prepare_accession_table,
    is_merge_size_zero,
    get_amdir_tags,
)


st.set_page_config(
    page_title="AMDirT Filter",
    page_icon="https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/master/assets/images/logos/spaam-AncientMetagenomeDir_logo_mini.png",
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

tags = get_amdir_tags() + ["master"]

with open(args.config) as c:
    tables = json.load(c)
    samples = tables["samples"]
    libraries = tables["libraries"]

# Sidebar
with st.sidebar:
    st.markdown(
        """
<p style="text-align:center;"><img src="https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/master/assets/images/logos/spaam-AncientMetagenomeDir_logo_colourmode.svg" alt="logo" width="50%"></p>
""",
        unsafe_allow_html=True,
    )
    st.write(f"# [AMDirT](https://github.com/SPAAM-community/AMDirT) filter tool")
    st.write(f"\n Version: {__version__}")
    st.write("## Select an AncientMetagenomeDir release")
    st.session_state.tag_name = st.selectbox(label="", options=tags)
    st.write("## Select a table")
    options = ["No table selected"] + list(samples.keys())
    st.session_state.table_name = st.selectbox(label="", options=options)
    st.write(f"Only {' and '.join(supported_archives)} archives are supported for now")
    st.write("## Select a download methods")
    st.session_state.dl_method = st.selectbox(
        label="", options=["curl", "nf-core/fetchngs"]
    )

if st.session_state.table_name != "No table selected":
    # Main content
    st.markdown(f"AncientMetagenomeDir release: `{st.session_state.tag_name}`")
    st.markdown(f"Displayed table: `{st.session_state.table_name}`")
    samp_url = samples[st.session_state.table_name].replace(
        "master", st.session_state.tag_name
    )
    lib_url = libraries[st.session_state.table_name].replace(
        "master", st.session_state.tag_name
    )
    print(samp_url)
    df = pd.read_csv(
        samp_url,
        sep="\t",
    )
    library = pd.read_csv(
        lib_url,
        sep="\t",
    )
    height = 50
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        groupable=True,
        value=True,
        enableRowGroup=True,
        aggFunc="sum",
        editable=False,
        filterParams={"inRangeInclusive": "true"},
    )
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_grid_options(checkboxSelection=True)
    gb.configure_pagination(
        enabled=True, paginationAutoPageSize=False, paginationPageSize=height
    )
    gb.configure_column(
        "project_name",
        headerCheckboxSelection=True,
        headerCheckboxSelectionFilteredOnly=True,
    )
    gridOptions = gb.build()

    with st.form("Samples table") as f:
        st.markdown("Select samples to filter")
        df_mod = AgGrid(
            df,
            gridOptions=gridOptions,
            data_return_mode="filtered",
            update_mode="selection_changed",
        )
        if st.form_submit_button("Validate selection", emphasis="primary"):
            if len(df_mod["selected_rows"]) == 0:
                st.error(
                    "You didn't select any sample! Please select at least one sample."
                )
            else:
                st.session_state.compute = True

    merge_is_zero = is_merge_size_zero(
        pd.DataFrame(df_mod["selected_rows"]), library, st.session_state.table_name
    )

    if (
        st.session_state.compute
        and not merge_is_zero
        and pd.DataFrame(df_mod["selected_rows"]).shape[0] != 0
    ):
        # if pd.DataFrame(df_mod["selected_rows"]).shape[0] == df.shape[0]:
        #     st.warning(
        #         "All samples are selected, are you sure you want you want them all ?"
        #     )
        #     st.session_state.force_validation = False
        #     if st.button("Yes"):
        #         st.session_state.force_validation = True
        # else:
        nb_sel_samples = pd.DataFrame(df_mod["selected_rows"]).shape[0]
        st.write(f"{nb_sel_samples } sample{'s'[:nb_sel_samples^1]} selected")
        st.session_state.force_validation = True
        placeholder = st.empty()
        with placeholder.container():
            fastq_button, samplesheet_button, bibtext_button = st.columns(3)
            if st.session_state.force_validation:
                if st.session_state.dl_method == "nf-core/fetchngs":
                    with fastq_button:
                        st.download_button(
                            label="Download nf-core/fetchNGS input accession list",
                            data=prepare_accession_table(
                                pd.DataFrame(df_mod["selected_rows"]),
                                library,
                                st.session_state.table_name,
                                supported_archives,
                            )["df"]
                            .to_csv(sep="\t", header=False, index=False)
                            .encode("utf-8"),
                            file_name="ancientMetagenomeDir_accession_table.csv",
                        )
                else:
                    with fastq_button:
                        st.download_button(
                            label="Download Curl sample download script",
                            data=prepare_accession_table(
                                pd.DataFrame(df_mod["selected_rows"]),
                                library,
                                st.session_state.table_name,
                                supported_archives,
                            )["script"],
                            file_name="ancientMetagenomeDir_curl_download_script.sh",
                        )
                with bibtext_button:
                    st.download_button(
                        label="Download Citations as BibTex",
                        data=prepare_bibtex_file(pd.DataFrame(df_mod["selected_rows"])),
                        file_name="ancientMetagenomeDir_citations.bib",
                    )
                if st.button("Start New Selection", type='primary'):
                    st.session_state.compute = False
                    st.session_state.table_name = "No table selected"
                    st.session_state.force_validation = False
                    # st.session_state.tag_name = tags[0]
                    placeholder.empty()
