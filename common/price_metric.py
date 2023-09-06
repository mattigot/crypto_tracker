import streamlit as st  # pip install streamlit
from config import *


def display_coin_container(df):
    filter_df = df[df[CFG_STR_CMC_SYMBOL].isin(CFG_UPPER_BAR_DISPLAY_COINS)]
    selected_columns = [CFG_STR_CMC_SYMBOL, CFG_STR_CMC_PRICE, CFG_STR_CMC_CHANGE_24H]

    coin_info = filter_df[selected_columns].to_dict(orient='records')

# Create a horizontal layout container
    with st.container():
        cols = st.columns(len(coin_info), gap = "small")

        i = 0
        for  col in cols:
            formated_value = format(round(coin_info[i][CFG_STR_CMC_PRICE]), ",")
            formated_delta = f"{coin_info[i][CFG_STR_CMC_CHANGE_24H] / 100:.2%}"

            col.metric(label=coin_info[i][CFG_STR_CMC_SYMBOL], value=formated_value, delta=formated_delta)
            i +=1 

    st.divider() 



