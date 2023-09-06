import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit
import subprocess

from config import *
from common.price_metric import *
from common.refresh_button import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Crypto Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
#@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="data.xlsx",
        engine="openpyxl",
        sheet_name="Sheet1",
        skiprows=0,
        usecols="A:BD",
        nrows=100,
    )
    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour

    return df
def get_data_from_csv(filename):
    df = pd.read_csv(filename)

    return df

df_w = get_data_from_csv(CFG_FILE_WATCHLIST_OUTPUT)
df_p = get_data_from_csv(CFG_FILE_PROTFOLIO_OUTPUT)

st.session_state['df'] = df_w
st.session_state['df_p'] = df_p

st.sidebar.image("misc/suppoman.png", use_column_width=True)
display_coin_container(df_w)
display_data_refresh_button()

# ---- SIDEBAR ----# Add a button to the sidebar
st.sidebar.header("Please Filter Here:")
risk = st.sidebar.multiselect(
    "Select the Risk:",
    options=df_w["Risk"].unique(),
    default=df_w["Risk"].unique()
)

stratergy = st.sidebar.multiselect(
    "Select the Strategy:",
    options=df_w["Strategy Tier"].unique(),
    default=df_w["Strategy Tier"].unique()
)

focus = st.sidebar.multiselect(
    "Select the Focus List:",
    options=df_w["Focus List"].unique(),
    default=1
)

df_selection = df_w.query(
    "Risk == @risk"
    #"Risk == @risk & 'Strategy Tier' ==@stratergy & 'Focus List' == @focus"
)


st.dataframe(df_selection)
