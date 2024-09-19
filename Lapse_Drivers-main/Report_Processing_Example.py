# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 19:30:56 2024

@author: Janco
"""

import shap
import matplotlib.pyplot as plt
import joblib

# Define function to process shap values
def shap_value_processor(s_vals, col=None):
    if col:
        if len(s_vals.shape)>2:
            return s_vals[:, col, 1]
        else:
            return s_vals[:, col]
    else:
        if len(s_vals.shape)>2:
            return s_vals[:, :, 1]
        else:
            return s_vals
        
# Function to calculate Net Risk Reduction
def calc_net_risk_reduction(lapse_impact, sum_lapse_prob_change, implementation_cost):
    total_risk_change = lapse_impact*sum_lapse_prob_change
    total_risk_reduction = -total_risk_change
    net_risk_reduction = total_risk_reduction - implementation_cost
    return net_risk_reduction

# Net risk reduction for all different of the treatment (DOCUMENT_PAGES_FILLED)
def net_risk_red_for_treatment(prob_effects_sum, lapse_impact, implementation_cost):
    net_risk_reduction_list = []
    for sum_prob_change in prob_effects_sum:
        net_risk_reduction_list.append(calc_net_risk_reduction(lapse_impact,
                                                               sum_prob_change,
                                                               implementation_cost))
    return net_risk_reduction_list

# Import object with results
# INSTRUCTIONS ---------------------------------------
# Replace with the path below to locate report_values.pkl
# ---------------------------------------------------
loaded_obj = joblib.load("report_values.pkl")

# Get shap values
shap_values = loaded_obj['shap_values']

# INSTRUCTIONS ----------------------------------------
# Change column names if required
# shap_feature_names = shap_values.feature_names
# print(shap_feature_names)
# shap_feature_names[0] = 'PRODUCT_SATISFACTION'
# shap_values.feature_names = shap_feature_names
# ----------------------------------------------------

# Create a shap bar plot
shap.plots.bar(shap_value_processor(shap_values), max_display=20)

# Create a beeswarm plot
shap.plots.beeswarm(shap_value_processor(shap_values), max_display=20)

# Create shap scatter plots
shap.plots.scatter(shap_value_processor(shap_values, col='numeric_imputer__CLAIM_COUNT'))

# INSTRUCTIONS -----------------------
# Create additional scatter plots as required
# shap.plots.scatter(shap_value_processor(shap_values, col='_FEATURE_NAME'))
# -----------------------------------

# Calculate payoff for Business Strategy 1
causal_strat = loaded_obj['causal_details'][0]

# Define the lapse impact and implementation cost for strategy 1
# (can be changed in a report/application)
lapse_impact = 12000
implementation_cost = 50000

# Calculate the Net Risk Reduction under various treatment values
nrr_list = net_risk_red_for_treatment(causal_strat['prob_effects_sum'],
                                      lapse_impact,
                                      implementation_cost
                                      )

# Visualise the Causal Effects
causal_feature = causal_strat['feature_name']
treatment_range = causal_strat['treatment_range']
plt.scatter(treatment_range, nrr_list)
plt.xlabel(causal_strat['x_label'])
plt.ylabel(causal_strat['y_label'])
plt.title(causal_strat['title'])
plt.show()


# Calculate payoff for Business Strategy 2
causal_strat = loaded_obj['causal_details'][1]

# Define the lapse impact and implementation cost for strategy 1
# (can be changed in a report/application)
lapse_impact = 12000
implementation_cost = 20000

# Calculate the Net Risk Reduction under various treatment values
nrr_list = net_risk_red_for_treatment(causal_strat['prob_effects_sum'],
                                      lapse_impact,
                                      implementation_cost
                                      )

# Visualise the Causal Effects
causal_feature = causal_strat['feature_name']
treatment_range = causal_strat['treatment_range']
plt.scatter(treatment_range, nrr_list)
plt.xlabel(causal_strat['x_label'])
plt.ylabel(causal_strat['y_label'])
plt.title(causal_strat['title'])
plt.show()

# Process the values for the hypothesis
hypo_1 = loaded_obj['hypothesis_list'][0]
hypo_1_descr = hypo_1['descr']

print("Hypothesis: ", hypo_1_descr)

# Calcute Shapley Scatter Plots to support hypothesis
shap.plots.scatter(shap_value_processor(loaded_obj['shap_values'],
                                        col=hypo_1['feature_name']))



















