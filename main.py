#--------------------             
# Author : Serge Zaugg
# Description : Create datasets, train models, assess performance
#--------------------

from utils import plot_scenarios, evaluate_scenarios_rfo, evaluate_scenarios_logit, plot_performance_vs_n_features
import os

# Define parameters 
random_seed = 557
path_save_figures = "./saved_figures_temp"
N = 3000
nb_noisy_features = [0, 1, 5, 10, 25, 50, 100, 500]
nb_trees = 30

# Define scenarios 
scenarios_di = { 
    "f01, f02 informative" : {
        'n1' : N, 'mu1' : [0.0, 2.0] , 'std1' : [1.1,1.1], 'corr1' : 0.00,
        'n2' : N, 'mu2' : [2.0, 0.0] , 'std2' : [1.0,1.0], 'corr2' : 0.00,},
    "f01, f02 informative and redundant" : {
        'n1' : N, 'mu1' : [ 1.4,  1.4] , 'std1' : [1,1], 'corr1' : +0.98,
        'n2' : N, 'mu2' : [-1.4, -1.4] , 'std2' : [1,1], 'corr2' : +0.98,},
    "f01, f02 jointly informative (parallel)" : {
        'n1' : N, 'mu1' : [-0.14, -0.14] , 'std1' : [1.2,1.2], 'corr1' : -0.98,
        'n2' : N, 'mu2' : [+0.14, +0.14] , 'std2' : [1.2,1.2], 'corr2' : -0.98,},
   "f01, f02 jointly informative (cross)" : {
        'n1' : N, 'mu1' : [0.0, 0.0] , 'std1' : [1,1], 'corr1' : -0.96,
        'n2' : N, 'mu2' : [0.0, 0.0] , 'std2' : [1,1], 'corr2' : +0.96,},
    "Only f01 is informative " : {
        'n1' : N, 'mu1' : [ 1.0, 1.0] , 'std1' : [1,1], 'corr1' : 0.00,
        'n2' : N, 'mu2' : [-1.0, 1.0] , 'std2' : [1,1], 'corr2' : 0.00,},
    "Features are NOT informative" : {
        'n1' : N, 'mu1' : [0.0, 0.0] , 'std1' : [1,1], 'corr1' : -0.90,
        'n2' : N, 'mu2' : [0.0, 0.0] , 'std2' : [1,1], 'corr2' : -0.90,}, 
    }

# prepare a temp dir to store results 
if not os.path.exists(path_save_figures):
    os.makedirs(path_save_figures)

# Prepare scenario figures  
figs_li = plot_scenarios(scenarios_di, random_seed,  width = 555, height = 460,)

resu01 = evaluate_scenarios_rfo(rfo_max_features =  1,    sce = scenarios_di, nb_noisy_features = nb_noisy_features, ntrees = nb_trees, seed = random_seed)
resu02 = evaluate_scenarios_rfo(rfo_max_features = 10,    sce = scenarios_di, nb_noisy_features = nb_noisy_features, ntrees = nb_trees, seed = random_seed)
resu03 = evaluate_scenarios_rfo(rfo_max_features = 25,    sce = scenarios_di, nb_noisy_features = nb_noisy_features, ntrees = nb_trees, seed = random_seed)
resu04 = evaluate_scenarios_logit(logit_c_param = 0.01,   sce = scenarios_di, nb_noisy_features = nb_noisy_features, seed = random_seed)
resu05 = evaluate_scenarios_logit(logit_c_param = 1.00,   sce = scenarios_di, nb_noisy_features = nb_noisy_features, seed = random_seed)
resu06 = evaluate_scenarios_logit(logit_c_param = 100.00, sce = scenarios_di, nb_noisy_features = nb_noisy_features, seed = random_seed)

# Prepare results figures 
fig01 = plot_performance_vs_n_features(resu01, width = 570, height = 750)
fig02 = plot_performance_vs_n_features(resu02, width = 570, height = 750)
fig03 = plot_performance_vs_n_features(resu03, width = 570, height = 750)
fig04 = plot_performance_vs_n_features(resu04, width = 570, height = 750)
fig05 = plot_performance_vs_n_features(resu05, width = 570, height = 750)
fig06 = plot_performance_vs_n_features(resu06, width = 570, height = 750)

# Save all figures for later re-import 
for i,f in enumerate(figs_li):
    f.write_image(os.path.join(path_save_figures, 'scenario' + str(i) + '.png' ) )  
fig01.write_image(os.path.join(path_save_figures, "results_01.png"))
fig02.write_image(os.path.join(path_save_figures, "results_02.png"))
fig03.write_image(os.path.join(path_save_figures, "results_03.png"))
fig04.write_image(os.path.join(path_save_figures, "results_04.png"))
fig05.write_image(os.path.join(path_save_figures, "results_05.png"))
fig06.write_image(os.path.join(path_save_figures, "results_06.png"))

# Render all figures directly in this session
if False:
    [f.show() for f in figs_li]
    fig01.show()
    fig02.show()
    fig03.show()
    fig04.show()
    fig05.show()
    fig06.show()




