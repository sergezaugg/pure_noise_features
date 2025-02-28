#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
#--------------------

import streamlit as st

st.set_page_config(layout="wide")

p0 = st.Page("st_page_00.py", title="Description")
p1 = st.Page("st_page_01.py", title="Interactive")

pg = st.navigation([p0, p1])

pg.run()

# run locally
# streamlit run stmain.py