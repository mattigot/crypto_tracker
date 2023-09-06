import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots
import streamlit as st  # pip install streamlit
from config import *
from common.price_metric import *


import streamlit as st

df = st.session_state['df']



display_coin_container(df)
