import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit

from config import *
from common.price_metric import *
from common.refresh_button import *
from common.data_filter import *

def create_charts(titles, gainers, losers):
    fig = make_subplots(rows=2, cols=2, subplot_titles=titles)

    for i, (col_name, gainers_df) in enumerate(gainers.items()):
        bar_gainers = px.bar(gainers_df, x="name", y=col_name, title=f"top 5 gainers - {col_name}", color_discrete_map={"name": "green"})
        #bar_trace = go.Bar(x=data["name"], y=data["value"], text=data["value"], textposition="auto", marker_color="green")
        fig.add_trace(bar_gainers.data[0], row=1, col=i+1)
        #fig.add_trace(bar_trace, row=1, col=1)

        losers_df = losers[col_name]
        bar_losers = px.bar(losers_df, x="name", y=col_name, title=f"top 5 losers - {col_name}", color_discrete_map={"name": "green"})
        fig.add_trace(bar_losers.data[0], row=2, col=i+1)

    fig.update_layout(height=600,  showlegend=False)

    return fig

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Movers Dashboard", page_icon=":bar_chart:", layout="wide")

df = st.session_state['df']


display_coin_container(df)
display_data_refresh_button()
df = dispaly_filter_by_interest(df, "Coins to Display")

gainers_to_view = st.sidebar.slider("Gainers to view:", 1, len(df), 10)
losers_to_view = st.sidebar.slider("Losers to view:", 1, len(df), 10)

top_gainers_r0 = {
    CFG_STR_CMC_CHANGE_1H: df.nlargest(gainers_to_view, CFG_STR_CMC_CHANGE_1H),
    CFG_STR_CMC_CHANGE_24H: df.nlargest(gainers_to_view, CFG_STR_CMC_CHANGE_24H)
}

top_gainers_r1 = {
    CFG_STR_CMC_CHANGE_7D: df.nlargest(gainers_to_view, CFG_STR_CMC_CHANGE_7D),
    CFG_STR_CMC_CHANGE_30D: df.nlargest(gainers_to_view, CFG_STR_CMC_CHANGE_30D)
}

top_gainers_r2 = {
    CFG_STR_CMC_CHANGE_60D: df.nlargest(gainers_to_view, CFG_STR_CMC_CHANGE_60D),
    CFG_STR_CMC_CHANGE_90D: df.nlargest(gainers_to_view, CFG_STR_CMC_CHANGE_90D)
}

top_losers_r0 = {
    CFG_STR_CMC_CHANGE_1H: df.nsmallest(losers_to_view, CFG_STR_CMC_CHANGE_1H),
    CFG_STR_CMC_CHANGE_24H: df.nsmallest(losers_to_view, CFG_STR_CMC_CHANGE_24H)
}

top_losers_r1 = {
    CFG_STR_CMC_CHANGE_7D: df.nsmallest(losers_to_view, CFG_STR_CMC_CHANGE_7D),
    CFG_STR_CMC_CHANGE_30D: df.nsmallest(losers_to_view, CFG_STR_CMC_CHANGE_30D)
}

top_losers_r2 = {
    CFG_STR_CMC_CHANGE_60D: df.nsmallest(losers_to_view, CFG_STR_CMC_CHANGE_60D),
    CFG_STR_CMC_CHANGE_90D: df.nsmallest(losers_to_view, CFG_STR_CMC_CHANGE_90D)
}

titles_r0 = ["1h change", "24h change"]
titles_r1 = ["7d change", "30d change"]
titles_r2 = ["60d change", "90 change"]

st.plotly_chart(create_charts(titles_r0, top_gainers_r0, top_losers_r0), use_container_width=True)
st.plotly_chart(create_charts(titles_r1, top_gainers_r1, top_losers_r1), use_container_width=True)
st.plotly_chart(create_charts(titles_r2, top_gainers_r2, top_losers_r2), use_container_width=True)

