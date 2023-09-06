import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit

from config import *
from common.price_metric import *
from common.refresh_button import *
from common.data_filter import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
columns_to_display = [
        CFG_STR_CMC_SYMBOL,
        CFG_STR_CMC_NAME,
        CFG_STR_BUY,
        CFG_STR_BUY_MINIMAL_PERC_DROP,
        CFG_STR_BUY_OPTIMAL_PERC_DROP,
        #CFG_STR_BUY_GENERATIONAL_PERC_DROP,
        CFG_STR_BUY_60X_PERC_DROP,
        CFG_STR_BUY_MINIMAL,
        CFG_STR_BUY_OPTIMAL,
        #CFG_STR_BUY_GENERATIONAL,
        CFG_STR_BUY_60X,
        CFG_STR_CMC_PRICE]

st.set_page_config(page_title="CFG_STR_BUY/Sell Dashboard", page_icon=":bar_chart:", layout="wide")

df = st.session_state['df']

### Create Side and Top Bar ###
display_coin_container(df)
display_data_refresh_button()

# Create a slide bar so we can filter by buy levels
buy_max = df[CFG_STR_BUY].max()
buys_to_view = st.sidebar.slider("Buy Level", 1, buy_max, 3)

### Filter the data ###
# Only ones we want to buy
coins_to_buy = df[df[CFG_STR_BUY] > 0]
# Only ones under in the chosen level
coins_to_buy = coins_to_buy[coins_to_buy[CFG_STR_BUY] <= buys_to_view]
coins_to_buy = coins_to_buy.sort_values(by=CFG_STR_BUY, ascending=False)

df = dispaly_filter_by_interest(df, "BI Percentage drops")
drops_to_view = st.sidebar.slider("BI Amount to Dispaly", 1, len(df), 10)

### Create Visualisations ###
# Create a bar chart to visualize the coins to buy
fig = px.bar(coins_to_buy, x=CFG_STR_CMC_SYMBOL, y=CFG_STR_BUY, title='Coins to Buy', text=CFG_STR_BUY)  # Specify text='Buy'
st.plotly_chart(fig, use_container_width=True)
#fig.update_layout(yaxis_range=[0, 4])
st.divider() 

#================= % To Drop
min_bi = df.nsmallest(drops_to_view, CFG_STR_BUY_MINIMAL_PERC_DROP)
opt_bi = df.nsmallest(drops_to_view, CFG_STR_BUY_OPTIMAL_PERC_DROP)
#gen_bi = df.nsmallest(drops_to_view, CFG_STR_BUY_GENERATIONAL_PERC_DROP)
sixtey_bi = df.nsmallest(drops_to_view, CFG_STR_BUY_60X_PERC_DROP)

#fig = make_subplots(rows=2, cols=2, subplot_titles=("Minimal BI Drop %", "Opt BI Drop %", "Generational BI Drop %", "60X BI Drop %"))

#fig = make_subplots(rows=1, cols=2, subplot_titles=("Min", "Opt", "Gen", "60x"))
px_min = px.bar(min_bi, x='name', y=CFG_STR_BUY_MINIMAL_PERC_DROP, text=CFG_STR_BUY_MINIMAL_PERC_DROP, title='Minimal BI Drop %')
px_opt = px.bar(opt_bi, x='name', y=CFG_STR_BUY_OPTIMAL_PERC_DROP, text=CFG_STR_BUY_OPTIMAL_PERC_DROP, title='Optimal BI Drop %')
#px_gen = px.bar(opt_bi, x='name', y=CFG_STR_BUY_GENERATIONAL_PERC_DROP)
px_six = px.bar(sixtey_bi, x='name', y=CFG_STR_BUY_60X_PERC_DROP, text=CFG_STR_BUY_60X_PERC_DROP, title='60x BI Drop %')


#fig.add_trace(px_min.data[0], row=1, col=1)
#fig.add_trace(px_opt.data[0], row=1, col=2)
#fig.add_trace(px_gen.data[0], row=2, col=2)
#fig.add_trace(px_six.data[0], row=2, col=2)

st.plotly_chart(px_min, use_container_width=True)
st.plotly_chart(px_opt, use_container_width=True)
st.plotly_chart(px_six, use_container_width=True)

#fig.update_layout(height=600, showlegend=False)
#st.plotly_chart(fig, use_container_width=True)

# ================= Table
st.divider()
st.dataframe(coins_to_buy[columns_to_display])
