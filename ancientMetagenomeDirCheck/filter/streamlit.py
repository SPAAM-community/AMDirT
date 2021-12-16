from st_aggrid import AgGrid
import streamlit as st
import pandas as pd

st.write("## Original DataFrame")
df = pd.read_csv(
    "https://raw.githubusercontent.com/SPAAM-community/AncientMetagenomeDir/master/ancientmetagenome-hostassociated/ancientmetagenome-hostassociated.tsv",
    sep="\t",
)


df_mod = AgGrid(df, data_return_mode="filtered", update_mode="filtering_changed")

st.write("## Filtered DataFrame")
st.write(df_mod["data"])


st.download_button(
    label="Download filtered  CSV",
    data=df_mod["data"].to_csv().encode("utf-8"),
    file_name="data.csv",
)
