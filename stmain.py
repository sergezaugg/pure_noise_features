#--------------------             
# Author : Serge Zaugg
# Description : Main streamlit entry point
# Run locally : streamlit run stmain.py
#--------------------

import streamlit as st

st.set_page_config(layout="wide")

pages = {
    "NAVIGATION": [
        st.Page("st_page_00.py", title="Summary"),
        st.Page("st_page_01.py", title="Interactive"),
    ]
}

# :orange[**INTRODUCTION**]

pg = st.navigation(pages)

pg.run()

with st.sidebar:
    st.title(""); st.title(""); st.title(""); st.title(""); st.title(""); st.title(""); st.title("")
    st.title(""); st.title(""); st.title(""); st.title("") 
    st.markdown(''':gray[RELATED TOPICS]''')
    st.page_link("https://ml-performance-metrics.streamlit.app/", label=":gray[ml-performance-metrics]")
    st.page_link("https://featureimportance.streamlit.app/", label=":gray[feature-importance:red]")
