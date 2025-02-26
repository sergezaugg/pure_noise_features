#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import plotly.io as pio

with open("./saved_figures/results_01.json", 'r') as f:
    fig_res01 = pio.from_json(f.read())

with open("./saved_figures/results_02.json", 'r') as f:
    fig_res02 = pio.from_json(f.read())
    
with open("./saved_figures/results_03.json", 'r') as f:
    fig_res03 = pio.from_json(f.read())

with open("./saved_figures/scenario0.JSON", 'r') as f:
    fig_scena01 = pio.from_json(f.read())

st.plotly_chart(fig_res01)
st.plotly_chart(fig_res02)
st.plotly_chart(fig_res03)
st.plotly_chart(fig_scena01)

# run locally
# streamlit run stmain.py




