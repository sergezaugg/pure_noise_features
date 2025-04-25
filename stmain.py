#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st
import plotly.express as px
from streamlit import session_state as ss
from utils import scenarios_di

# initial session state
if 'fig01' not in ss:
    ss.fig01 = px.scatter(x = [0], y = [0], width = 10, height = 10)
if 'fig02' not in ss:
    ss.fig02 = "not_available" 
if 'fig03' not in ss:
    ss.fig03 = "not_available" 
if 'distr' not in ss:
    ss['distr'] = {'cus' : scenarios_di[0]}  
if 'par' not in ss: 
    ss['par'] = {
        'sce_index' : 0,
        'nn_feat' : [0, 1, 3, 10, 30, 100, 300, 1000]
        }

st.set_page_config(layout="wide")

pages = [
    st.Page("st_page_01.py", title="Interactive"),
    st.Page("st_page_00.py", title="Summary"),
    ]

pg = st.navigation(pages)

pg.run()

with st.sidebar:
    st.text("v1.1.x - improvements underway")
    st.title(""); st.title(""); st.title(""); st.title(""); st.title(""); st.title(""); st.title("")
    st.title(""); st.title(""); st.title(""); st.title("") 
    st.markdown(''':gray[RELATED TOPICS]''')
    st.page_link("https://ml-performance-metrics.streamlit.app/", label=":gray[ml-performance-metrics]")
    st.page_link("https://featureimportance.streamlit.app/", label=":gray[feature-importance:red]")
