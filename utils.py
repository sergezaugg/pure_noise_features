#--------------------             
# Author : Serge Zaugg
# Description : Utility functions used by main.py
#--------------------

import os
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import streamlit as st

plotcol_seq01 = ['#0077ff', '#ffaa00', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000']
plotcol_seq02 = ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000']

# Define pre-specified scenarios 
N = 3000
scenarios_di = { 
    "Linearly separable I" : {
        'n1' : N, 'mu1' : [0.0, 2.0] , 'std1' : [1.1,1.1], 'corr1' : 0.00,
        'n2' : N, 'mu2' : [2.0, 0.0] , 'std2' : [1.0,1.0], 'corr2' : 0.00,
        },
    "Saurona" : {           
        'n1' : N, 'mu1' : [0.0, 0.0] , 'std1' : [1.2,1.2], 'corr1' : 0.0,
        'n2' : N, 'mu2' : [0.0, 0.0] , 'std2' : [0.05,0.7], 'corr2' : 0.0,
        },
    "Parallel" : {
        'n1' : N, 'mu1' : [-0.14, -0.14] , 'std1' : [1.2,1.2], 'corr1' : -0.98,
        'n2' : N, 'mu2' : [+0.14, +0.14] , 'std2' : [1.2,1.2], 'corr2' : -0.98,
        },
    "Cross" : {
        'n1' : N, 'mu1' : [0.0, 0.0] , 'std1' : [1.0, 1.0], 'corr1' : -0.96,
        'n2' : N, 'mu2' : [0.0, 0.0] , 'std2' : [1.0, 1.0], 'corr2' : +0.96,
        },
    "Linearly separable II" : {
        'n1' : N, 'mu1' : [ 1.0, 1.0] , 'std1' : [1.0,1.0], 'corr1' : 0.00,
        'n2' : N, 'mu2' : [-1.0, 1.0] , 'std2' : [1.0,1.0], 'corr2' : 0.00,
        },
    "Weak informative" : {
        'n1' : N, 'mu1' : [0.5, 0.0] , 'std1' : [1.0,1.0], 'corr1' : -0.90,
        'n2' : N, 'mu2' : [0.0, 0.0] , 'std2' : [1.0,1.0], 'corr2' : -0.90,
        }, 
   "Redundant" : {
        'n1' : N, 'mu1' : [ 1.4,  1.4] , 'std1' : [1.0,1.0], 'corr1' : +0.98,
        'n2' : N, 'mu2' : [-1.4, -1.4] , 'std2' : [1.0,1.0], 'corr2' : +0.98,
        }, 
   "Not separable" : {
        'n1' : N, 'mu1' : [0.0, 0.0] , 'std1' : [1.1,1.1], 'corr1' : 0.00,
        'n2' : N, 'mu2' : [0.0, 0.0] , 'std2' : [1.1,1.1], 'corr2' : 0.00,
        }, 
   "Looking up" : {
        'n1' : N, 'mu1' : [0.0, 0.0] , 'std1' : [1.0,1.0], 'corr1' : 0.0,
        'n2' : N, 'mu2' : [0.0, 1.0] , 'std2' : [0.15,0.1], 'corr2' : 0.0,
        }
    }





def str_to_int_spec(s):
    """
    Description: transform string s to integer, if not possible return 0 (Zero)
    """
    try:
        return(int(s))
    except:
        return(0)


def bivariate_normal(n = 1000, mu =[0,0] , std = [3,2], corr = 0.5):
    """ 
    """
    mu = np.array(mu)
    std = np.diag(np.array(std))
    sigma1 = np.array([[1.0,corr],[corr,1.0]])
    xtemp = np.matmul(sigma1, std)
    covar1 = np.matmul(std, xtemp)
    x1 = np.random.multivariate_normal(mean = mu, cov = covar1, size=n)
    return(x1)


@st.cache_data
def make_dataset(params, n_noisy_features): 
    """  
    """
    # create mvn data with controlled structure
    x1 = bivariate_normal(n = params['n1'], mu = params['mu1'] , std = params['std1'], corr = params['corr1'])
    x2 = bivariate_normal(n = params['n2'], mu = params['mu2'] , std = params['std2'], corr = params['corr2'])
    # add a class for supervised classification
    x1 = pd.DataFrame(x1, columns = ["f01", "f02"])
    x1["class"] = "Class A"
    x2 = pd.DataFrame(x2, columns = ["f01", "f02"])
    x2["class"] = "Class B"
    df = pd.concat([x1, x2])
    # re-order columns nicely 
    column_to_move = df.pop("class")
    df.insert(0, "class", column_to_move)
    df = df.reset_index(drop=True)
    # add multiple features that are uninformative for classification
    rand_feats = np.random.normal(0, 1, n_noisy_features*df.shape[0])
    rand_feats = rand_feats.reshape((df.shape[0], n_noisy_features))
    col_names = ['r'+str(a).zfill(3) for a in range(n_noisy_features)]
    df_rand_feats = pd.DataFrame(rand_feats, columns = col_names)
    df_rand_feats = df_rand_feats.reset_index(drop=True)
    # bring together the 2 informative an all the non-informative features 
    df = pd.concat([df, df_rand_feats], axis = 1)
    return(df)


# @st.cache_data
def plot_scenarios(scenarios_di, seed, width = 450, height = 450,):
    """
    """
    df_figs = []
    for k in scenarios_di:
        # print(k)
        mvn_params = scenarios_di[k]
        tit_str = 'Class A: N=' + str(mvn_params['n1']) + '   Class B: N=' + str(mvn_params['n2'])
        np.random.seed(seed = seed)
        df = make_dataset(params = mvn_params, n_noisy_features = 0) 
        fig1 = px.scatter(
            data_frame = df,
            x = 'f01',
            y = 'f02',
            color = 'class',
            width = width,
            height = height,
            title = tit_str,
            template="plotly_dark",
            color_discrete_sequence = plotcol_seq01,
            )         
        _ = fig1.update_xaxes(showline = True, linecolor = 'white', linewidth = 2, row = 1, col = 1, mirror = True)
        _ = fig1.update_yaxes(showline = True, linecolor = 'white', linewidth = 2, row = 1, col = 1, mirror = True)
        _ = fig1.update_traces(marker={'size': 2})
        _ = fig1.update_layout(paper_bgcolor="#111122")
        _ = fig1.update_layout(margin=dict(r=150, t=40 ))
        _ = fig1.update_layout(legend=dict(yanchor="top", y=0.9, xanchor="left", x=1.1)) 
        df_figs.append(fig1)
        # fig1.show()
    return(df_figs)    


@st.cache_data
def evaluate_scenarios_rfo(sce, nb_noisy_features, ntrees, rfo_max_features, seed):
    """
    """
    df_resu = []
    for k in sce:
        # print(k)
        mvn_params = sce[k]
        for counter, nb_noisfeat in enumerate(nb_noisy_features):
            # print(nb_noisfeat)
            np.random.seed(seed=seed)
            df = make_dataset(params = mvn_params, n_noisy_features = int(nb_noisfeat)) 
            # select predictors and response 
            X = df.iloc[:,1:]
            y = df['class']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.60)
            # initialize a model for supervised classification 
            clf = RandomForestClassifier(n_estimators=ntrees, max_depth=30, max_features = rfo_max_features, random_state=seed)
            clf.fit(X_train, y_train)
            # get overall performance as ROC-AUC
            y_pred = clf.predict_proba(X_test)[:,1]
            resu_auc = np.round(roc_auc_score(y_test, y_pred),2).item()
            df_t = pd.DataFrame([{"scenario": k, "nb_noisy_features": nb_noisfeat, "resu_auc": resu_auc,}])
            df_resu.append(df_t)
    df_final = pd.concat(df_resu)
    # keep track of params used 
    params = {
        'model_type' : 'RFO',
        'scenarios_di' : sce,
        'nb_noisy_features' : nb_noisy_features,
        'rfo_nb_trees' : ntrees,
        'rfo_max_features' : rfo_max_features,
        'random_seed' : seed,
        }
    return([df_final, params])


@st.cache_data
def evaluate_scenarios_logit(sce, nb_noisy_features, logit_c_param, seed):
    """
    """
    df_resu = []
    for k in sce:
        # print(k)
        mvn_params = sce[k]
        for counter, nb_noisfeat in enumerate(nb_noisy_features):
            # print(nb_noisfeat)
            np.random.seed(seed=seed)
            df = make_dataset(params = mvn_params, n_noisy_features = int(nb_noisfeat)) 
            # select predictors and response 
            X = df.iloc[:,1:]
            y = df['class']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.60)
            # initialize a model for supervised classification 
            clf = LogisticRegression(penalty = 'l2', C = logit_c_param, fit_intercept = True, random_state = seed)
            clf.fit(X_train, y_train)
            # get overall performance as ROC-AUC
            y_pred = clf.predict_proba(X_test)[:,1]
            resu_auc = np.round(roc_auc_score(y_test, y_pred),2).item()
            df_t = pd.DataFrame([{"scenario": k, "nb_noisy_features": nb_noisfeat, "resu_auc": resu_auc,}])
            df_resu.append(df_t)
    df_final = pd.concat(df_resu)
    # keep track of params used 
    params = {
        'model_type' : 'logitreg',
        'scenarios_di' : sce,
        'nb_noisy_features' : nb_noisy_features,
        'logit_c_param' : logit_c_param,
        'random_seed' : seed,
        }
    return([df_final, params])


@st.cache_data
def plot_performance_vs_n_features(li,  width = 500, height = 750):
    """
    """
    df  = li[0]
    par = li[1]
    # add small delt to 0 to allow log plot 
    df['nb_noisy_features'] = df['nb_noisy_features'].replace(to_replace=0, value=0.5)
    # plot 
    if par['model_type'] == 'RFO':
        pl_title = 'rfo_max_features: '  + str(par['rfo_max_features']) + '<br>' + 'rfo_nb_trees: ' + str(par['rfo_nb_trees'])
    if par['model_type'] == 'logitreg':
        pl_title = 'logistic C param: '  + str(par['logit_c_param']) 
    fig = px.line(
        data_frame = df,
        x = 'nb_noisy_features',
        y = 'resu_auc',
        color = 'scenario',
        width = width,
        height = height,
        markers=True,
        title = pl_title,
        template="plotly_dark",
        log_x = True,
        color_discrete_sequence = plotcol_seq02,
        )
    # dirty trick to be able to plot 0 on a logarithmic x axis 
    x_axis_num = fig['data'][0]['x']
    x_axis_str = x_axis_num.astype(int).astype(str)
    x_axis_str[0] = ' None (0)'
    fig.update_layout(xaxis = dict(tickmode='array', tickvals = x_axis_num, ticktext = x_axis_str,))
    # usual layout stuff
    _ = fig.update_layout(xaxis_title="Nb of pure-noise-features", yaxis_title="Predictive performance (AUC)")
    _ = fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.50, xanchor="left", x=0, font=dict(size=15)))
    _ = fig.update_xaxes(showline = True, linecolor = 'white', linewidth = 2, row = 1, col = 1, mirror = True)
    _ = fig.update_yaxes(showline = True, linecolor = 'white', linewidth = 2, row = 1, col = 1, mirror = True)
    _ = fig.update_layout(paper_bgcolor="#111122")
    _ = fig.update(layout_showlegend = False)
    # return fig object
    return(fig)









# devel 
if __name__ == "__main__":

    xx = bivariate_normal(n = 1000, mu =[1,1] , std = [1,1], corr = -0.9)
    xx.shape
    xx.std(0)
    pd.DataFrame(xx).corr()

    params = {
        'n1' : 100, 'mu1' : [0,0] , 'std1' : [1,1], 'corr1' : -0.9,
        'n2' : 100, 'mu2' : [0,0] , 'std2' : [1,1], 'corr2' : -0.9,
        }

    df = make_dataset(params = params, n_noisy_features = 1000) 

    df.head()
    df.shape

    "{:1.2f}".format(456.67895) # check 

