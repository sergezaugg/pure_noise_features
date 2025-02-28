# Impact of pure-noise-features on predictive performance in supervised classification

### Summary
This is a didactic mini-project.
In supervised classification applications, many features are typically available but we suspect that not all needed.
It is legitimate to ask which amount of un-informative feature is acceptable.
This small code base allows to simulate many scenario with variable number un-informative feature and see how they affect predictive performance.
**IN A NUTSHELL:**
A binary class variable and two informative features are created.
Many more pure-noise-features can be added the the feature space.
Random Forest Classifiers are trained on this data and their predictive performance (AUC) is computed.
Plots illustrate how pure-noise-features impacts the predictive performance.
**WORD OF CAUTION:**
The scenarios assessed here are artificial and by no way representative of situations encountered in the real world.
Yet, they are great way to didactically illustrate the subtle interactions between data and models.

**IN-DEPTH ILLUSTRATION:**
See link to Streamlit 

### Dependencies / Intallation
* Developed under Python 3.12.8
* First make a venv, then:
```
pip install -r requirements.txt
```

### Usage / Sample code
*  Below a mini example of how the code can be used to assess a few scenarios.
*  A more detailed sample code is found in **./main.py**

```python 
# import all functions and packages
from utils import plot_scenarios, evaluate_scenarios_rfo, plot_performance_vs_n_features

# Define several scenarios 
scenarios = { 
    "f01, f02 informative" : {
        'n1' : 5000, 'mu1' : [+0.00, +2.00], 'std1' : [1.00, 1.00], 'corr1' : +0.00,
        'n2' : 5000, 'mu2' : [+2.00, +0.00], 'std2' : [1.00, 1.00], 'corr2' : +0.00,
        },
    "f01, f02 jointly informative (parallel)" : {
        'n1' : 5000, 'mu1' : [-0.14, -0.14], 'std1' : [1.00, 1.00], 'corr1' : -0.98,
        'n2' : 5000, 'mu2' : [+0.14, +0.14], 'std2' : [1.00, 1.00], 'corr2' : -0.98,
        },
   "f01, f02 jointly informative (cross)" : {
        'n1' : 5000, 'mu1' : [+0.00, +0.00], 'std1' : [1.00, 1.00], 'corr1' : -0.98,
        'n2' : 5000, 'mu2' : [+0.00, +0.00], 'std2' : [1.00, 1.00], 'corr2' : +0.98,
        },
    }

# Prepare scenario figures  
figs_li = plot_scenarios(scenarios_di = scenarios, seed = 55)
# Evaluate the scenarios
resu00 = evaluate_scenarios_rfo(rfo_max_features = 1, sce = scenarios, 
    nb_noisy_features = [0, 5, 25, 50, 100, 500],  ntrees = 10, seed = 66)
# Prepare results figures 
fig00 = plot_performance_vs_n_features(resu00)
# Render all figures 
[f.show() for f in figs_li]
fig00.show()

```



