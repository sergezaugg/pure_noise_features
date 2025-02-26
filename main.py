#--------------------             
# Author : Serge Zaugg
# Description : Create synthetic datasets for classification, train models, assess classification performance
#--------------------

from utils import plot_scenarios, evaluate_scenarios, plot_performance_vs_n_features

import plotly.io as pio


random_seed = 557

# Define several scenarios 
scenarios_di = { 
    "f01, f02 informative" : {
        'n1' : 10000, 'mu1' : [0.0, 2.0] , 'std1' : [1,1], 'corr1' : 0.00,
        'n2' : 10000, 'mu2' : [2.0, 0.0] , 'std2' : [1,1], 'corr2' : 0.00,
        }
    ,
    "f01, f02 informative and redundant" : {
        'n1' : 10000, 'mu1' : [ 1.4,  1.4] , 'std1' : [1,1], 'corr1' : +0.98,
        'n2' : 10000, 'mu2' : [-1.4, -1.4] , 'std2' : [1,1], 'corr2' : +0.98,
        }
    ,
    "f01, f02 jointly informative (parallel)" : {
        'n1' : 10000, 'mu1' : [-0.14, -0.14] , 'std1' : [1,1], 'corr1' : -0.98,
        'n2' : 10000, 'mu2' : [+0.14, +0.14] , 'std2' : [1,1], 'corr2' : -0.98,
        }
    ,
   "f01, f02 jointly informative (cross)" : {
        'n1' : 10000, 'mu1' : [0.0, 0.0] , 'std1' : [1,1], 'corr1' : -0.98,
        'n2' : 10000, 'mu2' : [0.0, 0.0] , 'std2' : [1,1], 'corr2' : +0.98,
        }
    ,
    "Only f01 is informative " : {
        'n1' : 10000, 'mu1' : [ 1.0, 1.0] , 'std1' : [1,1], 'corr1' : 0.00,
        'n2' : 10000, 'mu2' : [-1.0, 1.0] , 'std2' : [1,1], 'corr2' : 0.00,
        }
    ,
    "Features are NOT informative" : {
        'n1' : 10000, 'mu1' : [0.0, 0.0] , 'std1' : [1,1], 'corr1' : -0.90,
        'n2' : 10000, 'mu2' : [0.0, 0.0] , 'std2' : [1,1], 'corr2' : -0.90,
        }
    , 
    }

# Prepare scenario figures  
figs_li = plot_scenarios(scenarios_di, random_seed)

# Evaluate the scenarios (QUICK)
nb_noisy_features = [0, 5, 25, 50, 100, 500]
nb_trees = 10
# Evaluate the scenarios (FULL)
# nb_noisy_features = [0, 1, 5, 10, 25, 50, 100, 500]
# nb_trees = 50
resu01 = evaluate_scenarios(scenarios_di, nb_noisy_features = nb_noisy_features,  rfo_nb_trees = nb_trees, rfo_max_features =  1, random_seed = random_seed)
resu02 = evaluate_scenarios(scenarios_di, nb_noisy_features = nb_noisy_features,  rfo_nb_trees = nb_trees, rfo_max_features = 10, random_seed = random_seed)
resu03 = evaluate_scenarios(scenarios_di, nb_noisy_features = nb_noisy_features,  rfo_nb_trees = nb_trees, rfo_max_features = 25, random_seed = random_seed)

# Prepare results figures 
fig01 = plot_performance_vs_n_features(resu01)
fig02 = plot_performance_vs_n_features(resu02)
fig03 = plot_performance_vs_n_features(resu03)

# Render all figures 
if False:
    [f.show() for f in figs_li]
    fig01.show()
    fig02.show()
    fig03.show()

# save all figures 
for i,f in enumerate(figs_li):
    pio.write_json(fig = f, file = 'saved_figures/scenario' + str(i) + '.JSON')

pio.write_json(fig = fig01, file = "./saved_figures/results_01.json")
pio.write_json(fig = fig02, file = "./saved_figures/results_02.json")
pio.write_json(fig = fig03, file = "./saved_figures/results_03.json")








