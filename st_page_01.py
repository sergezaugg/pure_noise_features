#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

from utils import plot_scenarios, evaluate_scenarios_rfo, evaluate_scenarios_logit, plot_performance_vs_n_features
import os
import streamlit as st
import plotly.express as px
from streamlit import session_state as ss

# initial value of session state
if 'fig01' not in ss:
    ss.fig01 = px.scatter(x = [0], y = [0], width = 10, height = 10)
if 'fig02' not in ss:
    ss.fig02 = px.scatter(x = [0], y = [0], width = 10, height = 10)
if 'fig03' not in ss:
    ss.fig03 = px.scatter(x = [0], y = [0], width = 10, height = 10)

random_seed = 0



a0, a1, = st.columns([0.60, 0.40])
with a0:
    with st.container(border=True, key='conta_01', height = 300):
        st.text("Distribution class A")
        c1, c2, c3, c4, c5, c6, = st.columns(6)   
        with c1:
            n1 = st.number_input(label = "N",  min_value=100, max_value=10000, value=3000, step=100, key = "k001")
        with c2:
            mu1x = st.number_input(label = "Mean X", min_value=-10.0, max_value=10.0, value=0.0,  key = "k002")
        with c3:
            mu1y = st.number_input(label = "Mean Y", min_value=-10.0, max_value=10.0, value=0.0,  key = "k003")
        with c4:
            std1x = st.number_input(label = "Stdev X", min_value=0.1, max_value=10.0, value=1.0,  key = "k004")
        with c5:
            std1y = st.number_input(label = "Stdev Y", min_value=0.1, max_value=10.0, value=1.0,  key = "k005")
        with c6:
            corr1 = st.number_input(label = "Correlation", min_value=-1.0, max_value=+1.0, value=0.0,  key = "k006")

        st.text("Distribution class B")
        c1, c2, c3, c4, c5, c6, = st.columns(6)
        with c1:
            n2 = st.number_input(label = "N",  min_value=100, max_value=10000, value=1000, step=100, label_visibility ="visible", key = "k007")
        with c2:
            mu2x = st.number_input(label = "Mean X", min_value=-10.0, max_value=10.0, value=0.0, label_visibility ="visible",key = "k008")
        with c3:
            mu2y = st.number_input(label = "Mean Y", min_value=-10.0, max_value=10.0, value=0.0, label_visibility ="visible",key = "k009")
        with c4:
            std2x = st.number_input(label = "Stdev X", min_value=0.1, max_value=10.0, value=0.1, label_visibility ="visible",key = "k010")
        with c5:
            std2y = st.number_input(label = "Stdev Y", min_value=0.1, max_value=10.0, value=1.0, label_visibility ="visible",key = "k011")
        with c6:
            corr2 = st.number_input(label = "Correlation", min_value=-1.0, max_value=+1.0, value=-0.0, label_visibility ="visible",key = "k012")

    with st.container(border=True, key='conta_01a', height = 185):
        c0, c1,  = st.columns(2)
        with c0:
            st.text("")   
            sttr = st.text_input("nb noisy features (comma sep)", "0, 5, 25, 50, 100")
            nb_noisy_features = sttr.split(",")
            nb_noisy_features = [int(a) for a in nb_noisy_features]
            nb_noisy_features.sort()
            st.text(nb_noisy_features)  


with a1:

    # Define several scenarios 
    scenarios_di = { 
    "custom scenario" : {
    'n1' : n1, 'mu1' : [mu1x, mu1y] , 'std1' : [std1x, std1y], 'corr1' : corr1,
    'n2' : n2, 'mu2' : [mu2x, mu2y] , 'std2' : [std2x, std2y], 'corr2' : corr2,
    }
    }

    with st.container(border=True, key='conta_02a', height = 500):
        figs_li = plot_scenarios(scenarios_di, random_seed, width = 530, height = 470,)
        ss["fig01"] = figs_li[0]        
        st.plotly_chart(ss["fig01"], use_container_width=False, key='k_fig01')
  




# with a0:
# with st.container(border=True, key='conta_02a'): # , height = 800):
#     figs_li = plot_scenarios(scenarios_di, random_seed, width = 500, height = 450,)
#     ss["fig01"] = figs_li[0]        
#     st.plotly_chart(ss["fig01"], use_container_width=False, key='k_fig01')


a0, a1, = st.columns([0.50, 0.50])

with a0:
    with st.container(border=True, key='conta_02b', height = 500):

        c1, c2,  = st.columns([0.20, 0.40], vertical_alignment="top")

        with c1:  
            st.subheader("Random Forest")
            nb_trees = st.number_input(label = "RF nb trees",  min_value=1, max_value=500, value=30, step=1,)
            rfo_max_features = st.number_input(label = "RF max features",  min_value=1, max_value=100, value=1, step=1)
            # compute the simulation 
            with st.form("B", border=False):
                submitted = st.form_submit_button("Start simulation")
                if submitted:   
                    resu02 = evaluate_scenarios_rfo(rfo_max_features = rfo_max_features, sce = scenarios_di, nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)
                    ss["fig02"] = plot_performance_vs_n_features(resu02, width = 680, height = 450)
                    ss["fig02"].update_layout(margin=dict(l=20, r=20, t=100, b=20),)
                    ss["fig02"].update_layout(yaxis_range=[0.49, +1.01])
        with c2:  
            st.plotly_chart(ss["fig02"], use_container_width=False, key='k_fig02')


with a1:               
    with st.container(border=True, key='conta_03', height = 500):

        c1, c2,  = st.columns([0.20, 0.40], vertical_alignment="top")

        with c1:  
            st.subheader("Logistic Regression")
            logit_c_param = st.number_input(label = "Logreg C (regularisation)",  min_value=0.0001, max_value=10000.000, value=1.000000, )
            # compute the simulation 
            with st.form("C", border=False):
                submitted = st.form_submit_button("Start simulation")
                if submitted:   
                    resu03 = evaluate_scenarios_logit(logit_c_param = logit_c_param, sce = scenarios_di, nb_noisy_features = nb_noisy_features, seed = random_seed)
                    ss["fig03"] = plot_performance_vs_n_features(resu03, width = 600, height = 450)
                    ss["fig03"].update_layout(margin=dict(l=20, r=20, t=100, b=20),)
                    ss["fig03"].update_layout(yaxis_range=[0.49, +1.01])
        with c2:  
            st.plotly_chart(ss["fig03"], use_container_width=False, key='k_fig03')    





