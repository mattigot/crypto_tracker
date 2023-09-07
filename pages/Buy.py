import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit

from config import *
from common.price_metric import *
from common.refresh_button import *
from common.data_filter import *

def highlight_cells(val):
    color = 'red' if val > 0 else 'green'
    return f'background-color: {color}'
 

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
columns_to_display = [
        CFG_STR_CMC_SYMBOL,
        CFG_STR_CMC_NAME,
        CFG_STR_BUY,
        CFG_STR_STRATERGAY_TIER,
        CFG_STR_BUY_MINIMAL_PERC_DROP,
        CFG_STR_BUY_OPTIMAL_PERC_DROP,
        #CFG_STR_BUY_GENERATIONAL_PERC_DROP,
        CFG_STR_BUY_60X_PERC_DROP,
        CFG_STR_BUY_MINIMAL,
        CFG_STR_BUY_OPTIMAL,
        #CFG_STR_BUY_GENERATIONAL,
        CFG_STR_BUY_60X,
        CFG_STR_CMC_PRICE]

bi_prices_to_display = [
    {'name': CFG_STR_BUY_MINIMAL_PERC_DROP, 'title': 'Minimal BI Drop %'},
    {'name': CFG_STR_BUY_OPTIMAL_PERC_DROP, 'title': 'Optimal BI Drop %'},
    {'name': CFG_STR_BUY_60X_PERC_DROP, 'title': '60X BI Drop %'},
]

st.set_page_config(page_title="CFG_STR_BUY/Sell Dashboard", page_icon=":bar_chart:", layout="wide")

# Embed an external website using an iframe
#st.write("Displaying an external website:")
#st.write("<iframe src='https://coinmarketcap.com/' width='800' height='600'></iframe>", unsafe_allow_html=True)
#st.components.v1.iframe("https://coinmarketcap.com/", width=800, height=600)

df = st.session_state['df']

### Create Side and Top Bar ###
display_coin_container(df)
display_data_refresh_button()


df = dispaly_filter_by_interest(df, "Filter")
coins_to_buy = df[df[CFG_STR_BUY] > 0]
coins_to_buy = coins_to_buy.sort_values(by=CFG_STR_BUY, ascending=False)

drops_to_view = st.sidebar.slider("Display", 1, len(df), 10)

### Create Visualisations ###
# Create a bar chart to visualize the coins to buy
fig = px.bar(coins_to_buy, x=CFG_STR_CMC_SYMBOL, y=CFG_STR_BUY, title='Coins to Buy', text=CFG_STR_BUY)  # Specify text='Buy'
st.plotly_chart(fig, use_container_width=True)
#fig.update_layout(yaxis_range=[0, 4])
st.divider() 

#================= % To Drop

colored_colomns = []
for tmp in bi_prices_to_display:
    #st.write(tmp)
    colored_colomns.append(tmp['name'])
    bi = df.nsmallest(drops_to_view, tmp['name'])
    px_bi = px.bar(bi, x='name', y=tmp['name'], text=tmp['name'], title=tmp['name'])
    st.plotly_chart(px_bi, use_container_width=True)

# ================= Table
st.divider()


df = df[columns_to_display]


st.dataframe(df.style.applymap(highlight_cells, subset=colored_colomns), height=1000)

