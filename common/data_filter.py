import streamlit as st  # pip install streamlit
from config import *

def dispaly_filter_by_interest(df, title):
    coins_movers_filters = st.sidebar.selectbox("%s:" % title, [CFG_STR_BUY, CFG_STR_FOCUS_LIST, CFG_STR_INVESTMENT_PERCENT, "All"])

    if coins_movers_filters == CFG_STR_FOCUS_LIST:
        return df[df[CFG_STR_FOCUS_LIST] == 1]
    elif  coins_movers_filters == CFG_STR_BUY:
        return df[df[CFG_STR_BUY] != 0]
    elif  coins_movers_filters == CFG_STR_INVESTMENT_PERCENT:
        return df[df[CFG_STR_INVESTMENT_PERCENT] != ""]
    
    return df
     