#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

from utils import plot_scenarios, evaluate_scenarios_rfo, evaluate_scenarios_logit, plot_performance_vs_n_features
import os
import streamlit as st
import plotly.express as px
from streamlit import session_state as ss

with st.sidebar:
    st.write("💜")
    st.write("Author: Serge Zaugg")
    st.page_link("https://github.com/sergezaugg/pure_noise_features", label="Link - Python source code")

# initial value of session state
if 'fig01' not in ss:
    ss.fig01 = px.scatter(x = [0], y = [0], width = 10, height = 10)
if 'fig02' not in ss:
    ss.fig02 = px.scatter(x = [0], y = [0], width = 10, height = 10)

random_seed = 0

c1, c2, c3, c4, c5, c6, = st.columns(6)
with c1:
    n1 = st.number_input(label = "n1",  min_value=100, max_value=10000, value=1000, step=100,)
with c2:
    mu1x = st.number_input(label = "mu1x", min_value=-10.0, max_value=10.0, value=0.0, )
with c3:
    mu1y = st.number_input(label = "mu1y", min_value=-10.0, max_value=10.0, value=0.0, )
with c4:
    std1x = st.number_input(label = "std1x", min_value=0.1, max_value=10.0, value=1.0, )
with c5:
    std1y = st.number_input(label = "std1y", min_value=0.1, max_value=10.0, value=1.0, )
with c6:
    corr1 = st.number_input(label = "corr1", min_value=-1.0, max_value=+1.0, value=0.8, )

c1, c2, c3, c4, c5, c6, = st.columns(6)
with c1:
    n2 = st.number_input(label = "n2",  min_value=100, max_value=10000, value=1000, step=100,)
with c2:
    mu2x = st.number_input(label = "mu2x", min_value=-10.0, max_value=10.0, value=0.0, )
with c3:
    mu2y = st.number_input(label = "mu2y", min_value=-10.0, max_value=10.0, value=0.0, )
with c4:
    std2x = st.number_input(label = "std2x", min_value=0.1, max_value=10.0, value=1.0, )
with c5:
    std2y = st.number_input(label = "std2y", min_value=0.1, max_value=10.0, value=1.0, )
with c6:
    corr2 = st.number_input(label = "corr2", min_value=-1.0, max_value=+1.0, value=-0.8, )

# Define several scenarios 
    scenarios_di = { 
    "custom scenario" : {
    'n1' : n1, 'mu1' : [mu1x, mu1y] , 'std1' : [std1x, std1y], 'corr1' : corr1,
    'n2' : n2, 'mu2' : [mu2x, mu2y] , 'std2' : [std2x, std2y], 'corr2' : corr2,
    }
    }

st.divider()

c0, c_1, c1, c_2, c2,  = st.columns([0.30, 0.03, 0.10, 0.03,  0.40])

with c0:  
    # check scenario 
    with st.form("A", border=False):
        submitted = st.form_submit_button("Show scatterplot")
        if submitted:
            figs_li = plot_scenarios(scenarios_di, random_seed, width = 450, height = 450,)
            ss["fig01"] = figs_li[0]
            
    st.plotly_chart(ss["fig01"], use_container_width=False, key='k_fig01')


with c_1: 
    st.title("  ")
    st.title("")
    st.title("")
    st.image(image = "./icons/arrow.png", width=30, use_container_width=False)


with c1:  
    st.title("")   
    sttr = st.text_input("nb noisy features (comma sep)", "0, 5, 25, 50, 100")
    nb_noisy_features = sttr.split(",")
    nb_noisy_features = [int(a) for a in nb_noisy_features]
    st.text(nb_noisy_features)
    nb_trees = st.number_input(label = "nb trees",  min_value=1, max_value=500, value=30, step=1,)
    rfo_max_features = st.number_input(label = "max features",  min_value=1, max_value=100, value=1, step=1)


with c_2: 
    st.title("  ")
    st.title("")
    st.title("")
    st.image(image = "./icons/arrow.png", width=30, use_container_width=False)


with c2:  
    # compute the simulation 
    with st.form("B", border=False):
        submitted = st.form_submit_button("Start simulation")
        if submitted:   
            resu02 = evaluate_scenarios_rfo(rfo_max_features = rfo_max_features, sce = scenarios_di, nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)
            ss["fig02"] = plot_performance_vs_n_features(resu02, width = 600, height = 450)
            ss["fig02"].update_layout(margin=dict(l=20, r=20, t=100, b=20),)
            ss["fig02"].update_layout(yaxis_range=[0.45, +1.1])

    st.plotly_chart(ss["fig02"], use_container_width=False, key='k_fig02')
        
st.divider()


