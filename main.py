#--------------------             
# Author : Serge Zaugg
# Description : Create synthetic datasets, train models, assess performance
#--------------------

from utils import plot_scenarios, evaluate_scenarios_rfo, evaluate_scenarios_logit, plot_performance_vs_n_features
import os

random_seed = 557
path_save_figures = "./saved_figures_temp"

# Define several scenarios 
scenarios_di = { 
    "f01, f02 informative" : {
        'n1' : 10000, 'mu1' : [0.0, 2.0] , 'std1' : [1.1,1.1], 'corr1' : 0.00,
        'n2' : 10000, 'mu2' : [2.0, 0.0] , 'std2' : [1.0,1.0], 'corr2' : 0.00,
        }
    ,
    "f01, f02 informative and redundant" : {
        'n1' : 10000, 'mu1' : [ 1.4,  1.4] , 'std1' : [1,1], 'corr1' : +0.98,
        'n2' : 10000, 'mu2' : [-1.4, -1.4] , 'std2' : [1,1], 'corr2' : +0.98,
        }
    ,
    "f01, f02 jointly informative (parallel)" : {
        'n1' : 10000, 'mu1' : [-0.14, -0.14] , 'std1' : [1.2,1.2], 'corr1' : -0.98,
        'n2' : 10000, 'mu2' : [+0.14, +0.14] , 'std2' : [1.2,1.2], 'corr2' : -0.98,
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
# nb_noisy_features = [0, 5, 25, 50, 100, 500]
# nb_trees = 10
# Evaluate the scenarios (FULL)
nb_noisy_features = [0, 1, 5, 10, 25, 50, 100, 500, 1000]
nb_trees = 50
resu01 = evaluate_scenarios_rfo(rfo_max_features =  1, sce = scenarios_di, nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)
resu02 = evaluate_scenarios_rfo(rfo_max_features = 10, sce = scenarios_di, nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)
resu03 = evaluate_scenarios_rfo(rfo_max_features = 25, sce = scenarios_di, nb_noisy_features = nb_noisy_features,  ntrees = nb_trees, seed = random_seed)
resu04 = evaluate_scenarios_logit(sce = scenarios_di, nb_noisy_features = nb_noisy_features, logit_c_param = 10.0, seed = random_seed)

# Prepare results figures 
fig01 = plot_performance_vs_n_features(resu01)
fig02 = plot_performance_vs_n_features(resu02)
fig03 = plot_performance_vs_n_features(resu03)
fig04 = plot_performance_vs_n_features(resu04)

# Save all figures later re-import 
for i,f in enumerate(figs_li):
    f.write_image(os.path.join(path_save_figures, 'scenario' + str(i) + '.png' ) )  #'saved_figures/scenario' + str(i) + '.png') 
fig01.write_image(os.path.join(path_save_figures, "results_01.png"))
fig02.write_image(os.path.join(path_save_figures, "results_02.png"))
fig03.write_image(os.path.join(path_save_figures, "results_03.png"))
fig04.write_image(os.path.join(path_save_figures, "results_04.png"))

# Render all figures directly in this session
if False:
    [f.show() for f in figs_li]
    fig01.show()
    fig02.show()
    fig03.show()
    fig04.show()



