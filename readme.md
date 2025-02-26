# Impact of pure-noise-features on predictive performance in supervised classification

**CONTEXT:**
This is a **didactic mini-project**
In supervised classification applications, many features are available but we suspect that not all needed.
Finding every last non-informative feature if often not feasible.
It is legitimate to ask which amount of un-informative feature is acceptable.

**ML SUMMARY:**
A binary class variable and two features that inform classification are created.
Many more pure-noise-features can be added the the feature space.
Random Forest Classifiers are trained on this data and their predictive performance (AUC) is computed on a test set.
Plots are made to illustrate how pure-noise-features impacts the predictive performance.

**WHY RANDOM FOREST:**
RF was chosen because it can handle non-linear problems, is robust to feature scale, its hyper-parameters ar easy to tune.
RF has one very important hyper-parameter: **max_features** which is the number of features to consider during search of best split.
Setting **max_features** to 1 mean at each split the feature to use is chosen at random.

**WORD OF CAUTION:**
The scenarios assessed here are artificial and by no way representative of  situations encountered in the real world.
Yet, they are great way to didactically illustrate the subtle interactions between data and models.

## Illustration of possible scenarios
*  Only the two first features are show
*  All other features are sampled from exactly the same random normal for both classes

![](./pics/sce_all6.png)

## Result from the 6 scenarios above
*  Predictive performance is measured with the AUC from test set (Y axis)
*  Inclusion of more pure-noise-features did negatively impact performance in most scenarios
*  A small to moderate amount of pure-noise-features often had no measurable impact on performance
*  The scenarios with joint information in f01 and f02 seem more vulnerable to pure-noise-features
*  Increasing **max_features** parameter of RF made the models more robust to pure-noise-features

![](./pics/resu_010203.png)


### Usage / Sample code
*  Below a mini example of how the code can be used to assess a few scenarios.
*  A more detailed sample code is found in **./main.py**

```python 
from utils import plot_scenarios, evaluate_scenarios, plot_performance_vs_n_features

random_seed = 5768

# Define several scenarios 
scenarios_di = { 
    "f01, f02 informative" : {
        'n1' : 10000, 'mu1' : [0.0, 2.0] , 'std1' : [1,1], 'corr1' : 0.00,
        'n2' : 10000, 'mu2' : [2.0, 0.0] , 'std2' : [1,1], 'corr2' : 0.00,
        },
    "f01, f02 jointly informative (parallel)" : {
        'n1' : 10000, 'mu1' : [-0.14, -0.14] , 'std1' : [1,1], 'corr1' : -0.98,
        'n2' : 10000, 'mu2' : [+0.14, +0.14] , 'std2' : [1,1], 'corr2' : -0.98,
        },
   "f01, f02 jointly informative (cross)" : {
        'n1' : 10000, 'mu1' : [0.0, 0.0] , 'std1' : [1,1], 'corr1' : -0.98,
        'n2' : 10000, 'mu2' : [0.0, 0.0] , 'std2' : [1,1], 'corr2' : +0.98,
        },
    }

# Prepare scenario figures  
figs_li = plot_scenarios(scenarios_di, random_seed)

# Evaluate the scenarios
resu00 = evaluate_scenarios(
    scenarios_di = scenarios_di, 
    nb_noisy_features = [0, 5, 25, 50, 100, 500],  
    rfo_nb_trees = 20, 
    rfo_max_features = 10, 
    random_seed = random_seed
    )

# Prepare results figures 
fig00 = plot_performance_vs_n_features(resu00)

# Render all figures 
[f.show() for f in figs_li]
fig00.show()
```


### Dependencies / Intallation
* Developed under Python 3.12.8
* First make a venv, then:
```
pip install -r requirements.txt
```

## ha
