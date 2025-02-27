#--------------------             
# Author : Serge Zaugg
# Description : Streamlit page 
#--------------------

from utils import plot_scenarios, evaluate_scenarios_rfo, evaluate_scenarios_logit, plot_performance_vs_n_features
import os
import streamlit as st

random_seed = 0


nb_noisy_features = [0, 5, 25, 50, 100]
nb_trees = 10

# Define several scenarios 
scenarios_di = { 
    "f01, f02 informative" : {
        'n1' : 10000, 'mu1' : [0.0, 2.0] , 'std1' : [1.1,1.1], 'corr1' : 0.00,
        'n2' : 10000, 'mu2' : [2.0, 0.0] , 'std2' : [1.0,1.0], 'corr2' : 0.00,
        }
    }


# Prepare scenario figures  
figs_li = plot_scenarios(scenarios_di, random_seed)
resu02 = evaluate_scenarios_rfo(rfo_max_features = 10, sce = scenarios_di, nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)

# Prepare results figures 
fig02 = plot_performance_vs_n_features(resu02)

# Render all figures directly in this session
# [f.show() for f in figs_li]
# fig02.show()
# fig04.show()

st.plotly_chart(fig02, use_container_width=False)
