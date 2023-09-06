import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit

from config import *
from common.price_metric import *
from common.refresh_button import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="CFG_STR_BUY/Sell Dashboard", page_icon=":bar_chart:", layout="wide")

df = st.session_state['df']

coins_to_buy = df[df[CFG_STR_BUY] > 0]
coins_to_buy = coins_to_buy.sort_values(by=CFG_STR_BUY, ascending=False)

columns_to_display = [
        CFG_STR_CMC_SYMBOL,
        CFG_STR_CMC_NAME,
        CFG_STR_BUY,
        CFG_STR_BUY_MINIMAL_PERC_DROP,
        CFG_STR_BUY_OPTIMAL_PERC_DROP,
        CFG_STR_BUY_GENERATIONAL_PERC_DROP,
        CFG_STR_BUY_60X_PERC_DROP,
        CFG_STR_BUY_MINIMAL,
        CFG_STR_BUY_OPTIMAL,
        CFG_STR_BUY_GENERATIONAL,
        CFG_STR_BUY_60X,
        CFG_STR_CMC_PRICE]

display_coin_container(df)
display_data_refresh_button()

# Create a bar chart to visualize the coins to buy
fig = px.bar(coins_to_buy, x=CFG_STR_CMC_SYMBOL, y=CFG_STR_BUY, title='Coins to Buy', text=CFG_STR_BUY)  # Specify text='Buy'
st.plotly_chart(fig, use_container_width=True)
fig.update_layout(yaxis_range=[0, 4])
st.divider() 
#================= % To Drop
min_bi = df.nsmallest(CFG_DROP_PERCENT_AMOUNT, CFG_STR_BUY_MINIMAL_PERC_DROP)
opt_bi = df.nsmallest(CFG_DROP_PERCENT_AMOUNT, CFG_STR_BUY_OPTIMAL_PERC_DROP)
gen_bi = df.nsmallest(CFG_DROP_PERCENT_AMOUNT, CFG_STR_BUY_GENERATIONAL_PERC_DROP)
sixtey_bi = df.nsmallest(CFG_DROP_PERCENT_AMOUNT, CFG_STR_BUY_60X_PERC_DROP)

fig = make_subplots(rows=2, cols=2, subplot_titles=("Minimal BI Drop %", "Opt BI Drop %", "Generational BI Drop %", "60X BI Drop %"))

#fig = make_subplots(rows=1, cols=2, subplot_titles=("Min", "Opt", "Gen", "60x"))
px_min = px.bar(min_bi, x='name', y=CFG_STR_BUY_MINIMAL_PERC_DROP)
px_opt = px.bar(opt_bi, x='name', y=CFG_STR_BUY_OPTIMAL_PERC_DROP)
px_gen = px.bar(opt_bi, x='name', y=CFG_STR_BUY_GENERATIONAL_PERC_DROP)
px_six = px.bar(opt_bi, x='name', y=CFG_STR_BUY_60X_PERC_DROP)


fig.add_trace(px_min.data[0], row=1, col=1)
fig.add_trace(px_opt.data[0], row=1, col=2)
fig.add_trace(px_gen.data[0], row=2, col=2)
fig.add_trace(px_six.data[0], row=2, col=2)


fig.update_layout(height=600, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ================= Table
st.divider()
st.dataframe(coins_to_buy[columns_to_display])
