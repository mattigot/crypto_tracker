import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit

from config import *
from common.price_metric import *
from common.refresh_button import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Movers Dashboard", page_icon=":bar_chart:", layout="wide")

df = st.session_state['df']

display_coin_container(df)
display_data_refresh_button()

top5_gainers = {
    CFG_STR_CMC_CHANGE_7D: df.nlargest(CFG_GAINERS_AMOUNT, CFG_STR_CMC_CHANGE_7D),
    CFG_STR_CMC_CHANGE_30D: df.nlargest(CFG_GAINERS_AMOUNT, CFG_STR_CMC_CHANGE_30D),
    CFG_STR_CMC_CHANGE_60D: df.nlargest(CFG_GAINERS_AMOUNT, CFG_STR_CMC_CHANGE_60D),
    CFG_STR_CMC_CHANGE_90D: df.nlargest(CFG_GAINERS_AMOUNT, CFG_STR_CMC_CHANGE_90D)
}

top5_losers = {
    CFG_STR_CMC_CHANGE_7D: df.nsmallest(CFG_LOSERS_AMOUNT, CFG_STR_CMC_CHANGE_7D),
    CFG_STR_CMC_CHANGE_30D: df.nsmallest(CFG_LOSERS_AMOUNT, CFG_STR_CMC_CHANGE_30D),
    CFG_STR_CMC_CHANGE_60D: df.nsmallest(CFG_LOSERS_AMOUNT, CFG_STR_CMC_CHANGE_60D),
    CFG_STR_CMC_CHANGE_90D: df.nsmallest(CFG_LOSERS_AMOUNT, CFG_STR_CMC_CHANGE_90D)
}

fig = make_subplots(rows=2, cols=4, subplot_titles=("7d change", "30d change", "60d change", "90 change"))

for i, (col_name, gainers_df) in enumerate(top5_gainers.items()):
    bar_gainers = px.bar(gainers_df, x="name", y=col_name, title=f"top 5 gainers - {col_name}", color_discrete_map={"name": "green"})
    fig.add_trace(bar_gainers.data[0], row=1, col=i+1)

    losers_df = top5_losers[col_name]
    bar_losers = px.bar(losers_df, x="name", y=col_name, title=f"top 5 losers - {col_name}", color_discrete_map={"name": "green"})
    fig.add_trace(bar_losers.data[0], row=2, col=i+1)

fig.update_layout(height=600, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

