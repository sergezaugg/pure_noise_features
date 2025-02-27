#--------------------             
# Author : Serge Zaugg
# Description : 
#--------------------

import os
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit import session_state as ss
import plotly.io as pio

# run locally
# streamlit run stmain.py

path_pics = "pics_dashboard"

# st.set_page_config(layout="wide") # "wide") centered

with st.sidebar:
    st.write("💜")
    st.write("Author: Serge Zaugg")
    st.page_link("https://github.com/sergezaugg/pure_noise_features", label="Link - Python source code")

col_a, col_space01 = st.columns([0.80, 0.20])


with col_a:

    st.title("Impact of pure-noise-features on predictive performance in supervised classification")     

    #----------------
    # xxx line 
    st.divider()

    st.header("Introduction")     
    st.markdown(''' 
    In supervised classification problems, many features are often available but we suspect that not all needed.
    Detecting and excluding every last non-informative feature if often not feasible.
    It is therefore legitimate to ask which amount of non-informative features is acceptable. 
    This mini-project gives some answers based on simulated data.
    **WORD OF CAUTION:** The scenarios assessed here are artificial and by no way representative of situations encountered in the real world.
    Yet, they are great way to didactically illustrate the subtle interactions between data and models.     
    ''')

    st.header("Methods")   
    st.markdown(''' 
    A binary class variable and two features that inform classification are created.
    Many pure-noise-features can be included in the feature space.
    They are non-informative for the classification task because they are sampled from the same random normal for both classes.
    Random Forest classifiers are trained on this data and their predictive performance (ROC-AUC) is computed with a test set.
    As a modeling method, the Random Forest was chosen because it can handle non-linear problems, it is robust to feature scale, and its hyper-parameters are easy to tune.
    Random Forest has one important hyper-parameter, **max_features**, which is the number of features to consider during search of best split.
    Setting **max_features** to 1 mean at each split the feature to use is chosen at random.
    Setting it to total number of features means that at each split all features are assessed and the best is chosen            
    Hence, higher values of **max_features** are expected to perform better in the presence of many pure-noise-features.          
    ''')

    st.header("Scenarios")   
    st.markdown(''' 
    Six scenarios were assessed as show in the figures below.
    Only the two informative features are shown on the plots.                    
    ''')
    col_a, col_b, col_c = st.columns([0.20, 0.20, 0.20])
    col_a.image(image = os.path.join(path_pics, 'scenario0.png'), caption="Figure 1", width=None, use_container_width=False)
    col_b.image(image = os.path.join(path_pics, 'scenario1.png'), caption="Figure 2", width=None, use_container_width=False)
    col_c.image(image = os.path.join(path_pics, 'scenario2.png'), caption="Figure 3", width=None, use_container_width=False)
    col_a, col_b, col_c = st.columns([0.20, 0.20, 0.20])
    col_a.image(image = os.path.join(path_pics, 'scenario3.png'), caption="Figure 4", width=None, use_container_width=False)
    col_b.image(image = os.path.join(path_pics, 'scenario4.png'), caption="Figure 5", width=None, use_container_width=False)
    col_c.image(image = os.path.join(path_pics, 'scenario5.png'), caption="Figure 6", width=None, use_container_width=False)


    st.header("Results and discussion")     
    st.markdown('''    
    Figures 7-9 illustrate how pure-noise-features impacts the predictive performance.
    *  Inclusion of more pure-noise-features did negatively impact performance in most scenarios
    *  A small to moderate amount of pure-noise-features often had no measurable impact on performance
    *  The scenarios with joint information in f01 and f02 seem more vulnerable to pure-noise-features
    *  Increasing **max_features** parameter of RF made the models more robust to pure-noise-features
    ''')
    col_a, col_b, col_c = st.columns([0.20, 0.20, 0.20])
    col_a.image(image = os.path.join(path_pics, 'results_01.png'), caption="Figure 7", width=None, use_container_width=False)
    col_b.image(image = os.path.join(path_pics, 'results_02.png'), caption="Figure 8", width=None, use_container_width=False)
    col_c.image(image = os.path.join(path_pics, 'results_03.png'), caption="Figure 9", width=None, use_container_width=False)

    #----------------
    # xxx line 
    st.divider()












