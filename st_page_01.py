#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

import streamlit as st
import plotly.express as px
from utils import plot_scenarios, evaluate_scenarios_rfo, evaluate_scenarios_logit, plot_performance_vs_n_features, str_to_int_spec
from utils import scenarios_di
from streamlit import session_state as ss

random_seed = 557

# initial session state
if 'fig01' not in ss:
    ss.fig01 = px.scatter(x = [0], y = [0], width = 10, height = 10)
if 'fig02' not in ss:
    ss.fig02 = "not_available" 
if 'fig03' not in ss:
    ss.fig03 = "not_available" 
if 'distr' not in ss:
    ss['distr'] = {'cus' : scenarios_di['Linearly separable I']}  


# ---------------------          
a0b, a1b, = st.columns([0.60, 0.40])
with a0b:

    with st.container(border=True, key='conta_b01'):
        with st.form(key = "f01", border=False):
            a0, a1, a2, _ = st.columns(4)  
            with a0:
                preset_options = list(scenarios_di.keys()) 
                option1 = st.selectbox("Predefined distributions", preset_options, key = 'sel02')
            with a1:
                st.text("")
                st.text("")
                submitted = st.form_submit_button("Confirm", type="primary", use_container_width = True)
            if submitted: 
                ss['distr'] = {'cus' : scenarios_di[option1]}

    with st.form("f02", border=False, clear_on_submit=False, enter_to_submit=False):
        with st.container(border=True, key='conta_01', height = 300):
            cc1, cc2, _, _ = st.columns(4)  
            with cc1:
                st.text("Finetune distribution class A")
            with cc2:
                submitted_1 = st.form_submit_button("Submit values", type="primary", use_container_width = True)
            c1, c2, c3, c4, c5, c6, = st.columns(6)  
            with c1:
                n1 = st.number_input(label = "N",  min_value=10, max_value=10000,               value=ss['distr']['cus']['n1'],      step=100, key = "k001")
            with c2:
                mu1x = st.number_input(label = "Mean X", min_value=-10.0, max_value=10.0,       value=ss['distr']['cus']['mu1'][0],  step=1.0, key = "k002")
            with c3:
                mu1y = st.number_input(label = "Mean Y", min_value=-10.0, max_value=10.0,       value=ss['distr']['cus']['mu1'][1],  step=1.0, key = "k003")
            with c4:
                std1x = st.number_input(label = "Stdev X", min_value=0.01, max_value=10.0,      value=ss['distr']['cus']['std1'][0], step=0.1, key = "k004")
            with c5:
                std1y = st.number_input(label = "Stdev Y", min_value=0.01, max_value=10.0,      value=ss['distr']['cus']['std1'][1], step=0.1, key = "k005")
            with c6:
                corr1 = st.number_input(label = "Correlation", min_value=-1.0, max_value=+1.0,  value=ss['distr']['cus']['corr1'],   step=0.1, key = "k006")
            st.text("Finetune distribution class B")
            c1, c2, c3, c4, c5, c6, = st.columns(6)
            with c1:
                n2 = st.number_input(label = "N",  min_value=10, max_value=10000,               value=ss['distr']['cus']['n2'],      step=100, key = "k007")
            with c2:
                mu2x = st.number_input(label = "Mean X", min_value=-10.0, max_value=10.0,       value=ss['distr']['cus']['mu2'][0],  step=1.0, key = "k008")
            with c3:
                mu2y = st.number_input(label = "Mean Y", min_value=-10.0, max_value=10.0,       value=ss['distr']['cus']['mu2'][1],  step=1.0, key = "k009")
            with c4:
                std2x = st.number_input(label = "Stdev X", min_value=0.01, max_value=10.0,      value=ss['distr']['cus']['std2'][0], step=0.1, key = "k010")
            with c5:
                std2y = st.number_input(label = "Stdev Y", min_value=0.01, max_value=10.0,      value=ss['distr']['cus']['std2'][1], step=0.1, key = "k011")
            with c6:
                corr2 = st.number_input(label = "Correlation", min_value=-1.0, max_value=+1.0,  value=ss['distr']['cus']['corr2'],   step=0.1, key = "k012")

            if submitted_1:
                ss['distr']['cus'] =  {
                    'n1' : n1, 'mu1' : [mu1x, mu1y] , 'std1' : [std1x, std1y], 'corr1' : corr1,
                    'n2' : n2, 'mu2' : [mu2x, mu2y] , 'std2' : [std2x, std2y], 'corr2' : corr2,
                    }
                st.rerun() # this solves the jump-back-button-glitch-wtf
    

# ---------------------          
    with st.container(border=True, key='conta_01a', height = 100):
        c0, c1, c2 = st.columns(3)
        with c0:
            sttr = st.text_input("Nb noisy features (comma separated)", "0, 1, 3, 10, 30, 100, 300, 1000")
            nb_noisy_features = sttr.split(",")
            nb_noisy_features = [str_to_int_spec(a) for a in nb_noisy_features] # convert to int if possible , else to ZERO
            nb_noisy_features.append(0) # force ZERO to be in
            nb_noisy_features = list(set(nb_noisy_features)) # remove duplicates
            nb_noisy_features.sort()
        with c1:
            st.text("Selected values")  
            st.text(nb_noisy_features)  
        with c2:
            st.text("")  



# ---------------------                         
with a1b:
    with st.container(border=True, key='conta_02a', height = 536):
        figs_li = plot_scenarios(ss['distr'], random_seed, width = 555, height = 460,)
        ss["fig01"] = figs_li[0]        
        st.plotly_chart(ss["fig01"], use_container_width=False, key='k_fig01')
  
a0, a1, = st.columns([0.50, 0.50])
with a0:
    with st.container(border=True, key='conta_02b', height = 440):
        c1, c2,  = st.columns([0.20, 0.40], vertical_alignment="top")
        with c1:  
            st.subheader("Random Forest")
            nb_trees = st.number_input(label = "RF nb trees",  min_value=1, max_value=500, value=30, step=1,)
            rfo_max_features = st.number_input(label = "RF max features",  min_value=1, max_value=100, value=1, step=1)
            # compute the simulation 
            with st.form("B", border=False):
                submitted = st.form_submit_button("Start simulation", type="primary")
                if submitted:   
                    resu02 = evaluate_scenarios_rfo(rfo_max_features = rfo_max_features, sce = ss['distr'], nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)
                    ss["fig02"] = plot_performance_vs_n_features(resu02, width = 680, height = 400)
                    ss["fig02"].update_layout(margin=dict(l=20, r=20, t=100, b=20),)
                    ss["fig02"].update_layout(yaxis_range=[0.40, +1.02])
            with c2:  
                if ss["fig02"] == "not_available":
                    print("plot not available")
                else:    
                    st.plotly_chart(ss["fig02"], use_container_width=False, key='k_fig02')
            
with a1:               
    with st.container(border=True, key='conta_03', height = 440):
        c1, c2,  = st.columns([0.20, 0.40], vertical_alignment="top")
        with c1:  
            st.subheader("Logistic Regression")
            logit_c_param = st.number_input(label = "Logreg C (regularisation)",  min_value=0.0001, max_value=10000.0, value=1.0)
            # compute the simulation 
            with st.form("C", border=False):
                submitted = st.form_submit_button("Start simulation", type="primary")
                if submitted:   
                    resu03 = evaluate_scenarios_logit(logit_c_param = logit_c_param, sce = ss['distr'], nb_noisy_features = nb_noisy_features, seed = random_seed)
                    ss["fig03"] = plot_performance_vs_n_features(resu03, width = 600, height = 400)
                    ss["fig03"].update_layout(margin=dict(l=20, r=20, t=100, b=20),)
                    ss["fig03"].update_layout(yaxis_range=[0.40, +1.02])
            with c2:  
                if ss["fig03"] == "not_available":
                    print("plot not available")
                else:                
                    st.plotly_chart(ss["fig03"], use_container_width=False, key='k_fig03')    





