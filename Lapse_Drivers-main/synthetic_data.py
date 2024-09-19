# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:37:18 2024

@author: Janco
"""

import pandas as pd
import random
from datetime import datetime
import numpy as np

def generate_random_feedback():
    feedback_options = [
        "I am very unsatisfied with the total amount of excess paid on my last claim.",
        "The claims process was smooth and quick, which I appreciate.",
        "The customer service team is hard to reach and not very helpful.",
        "I'm unsatisfied with the total amount of excess paid for my policy; it feels too high.",
        "I found the online portal difficult to navigate and access my policy information.",
        "The premiums seem to increase every year without explanation.",
        "Happy with the coverage provided, but the paperwork is excessive.",
        "I'm unsatisfied with the total amount of excess paid when I filed a claim last month.",
        "The waiting time for claim approval was too long.",
        "I'm generally happy with the service, but my policy feels overpriced.",
        "The excess fee is much higher than expected, which is frustrating.",
        "The customer service team was helpful in resolving my issue.",
        "I feel like I'm paying too much in premiums for the coverage I receive.",
        "I'm unsatisfied with the total amount of excess paid on my auto insurance claim.",
        "The communication regarding policy changes could be better.",
        "My claim was denied without proper explanation, and I’m disappointed.",
        "I appreciate the flexible payment options, but the excess fees are a concern.",
        "The process for updating my policy was confusing and took too long.",
        "I’m unsatisfied with the total amount of excess paid; it’s not aligned with what was initially promised.",
        "The coverage is good, but customer service needs improvement.",
        ]
    return random.choice(feedback_options)

def rating_effect(rating, coeff):
    if np.isnan(rating):
        return -10*coeff
    else:
        return rating*coeff
    
def set_nan_with_probability(variable, probability=0.1):
    if random.random() < probability:
        return np.nan
    else:
        return variable


def customer_service_lang_not_offered(language):
    if language=='Venda':
        return 1
    else:
        return 0

def detect_excess_dissatisfaction(feedback):
    if 'excess' in feedback:
        return 1
    else:
        return 0
    
def generate_random_date():
    # Define start and end years
    start_year = 2000
    end_year = 2024
    
    # Randomly select a year
    year = random.randint(start_year, end_year)
    
    # Randomly select a month
    month = random.randint(1, 12) if year != 2024 else random.randint(1, 8)  # up to August 2024

    # Create the datetime object set to the first of the month
    random_date = datetime(year, month, 1)
    
    return random_date


def create_synthetic_data(n=100):
    survey_cols = ['POL_NUMBER', 'MONTH_KEY', 'HOW_LIKELY_ARE_YOU_TO_RECOMMEND_THE_PRODUCT', 'GENERAL_FEEDBACK']
    cols = survey_cols # + lapse data
    
    df = pd.DataFrame()
    
    for n_i in range(0, n):
        new_row = {}
        
        # Generate POL_NUMBER and MONTH_KEY
        pol_num = 'P_'+str(n_i)
        month_key = generate_random_date()
        
        # Generate customer survey entry
        new_row['POL_NUMBER'] = pol_num
        new_row['MONTH_KEY'] = month_key
        new_row['HOW_LIKELY_ARE_YOU_TO_RECOMMEND_THE_PRODUCT'] = set_nan_with_probability(random.randint(1, 5))
        new_row['GENERAL_FEEDBACK'] = generate_random_feedback()
        
        # Generate lapse data
        new_row['POL_NUMBER_2'] = pol_num
        new_row['MONTH_KEY_2'] = month_key
        new_row['AGE'] = random.randint(18, 85)
        new_row['GENDER'] = random.choice(["M", "F"])
        
        # Generate other lapse fields
        new_row['CLAIM_COUNT'] = random.randint(1, 4)
        new_row['DOCUMENT_PAGES_FILLED'] = random.randint(4, 20)
        new_row['EXCESS_AMOUNT_CHOSEN'] = random.choice([0, 1500, 6000])
        new_row['NEWSLETTER_EMAIL_COUNT'] = random.randint(20, 50)
        new_row['WEBSITE_VISITS'] = random.randint(3, 25)
        new_row['HOME_LANGUAGE'] = random.choice(['English',
                                                  #'Afrikaans',
                                                  'isiZulu',
                                                  #'Xhosa',
                                                  'Venda',
                                                  'Venda',
                                                  'Venda'
                                                  ])
        new_row['ECONOMY_HEALTH_INDICATOR'] = random.randint(1, 5)
        
        # Create lapse indicator
        z = (
            + rating_effect(new_row['HOW_LIKELY_ARE_YOU_TO_RECOMMEND_THE_PRODUCT'],
                            coeff=-8.0)
            - 6*new_row['CLAIM_COUNT']
            + 2.5*new_row['DOCUMENT_PAGES_FILLED']
            + 100*detect_excess_dissatisfaction(new_row['GENERAL_FEEDBACK'])
            + 0.003*new_row['EXCESS_AMOUNT_CHOSEN']
            - 10*new_row['ECONOMY_HEALTH_INDICATOR']
            - 0.9*new_row['NEWSLETTER_EMAIL_COUNT']
            - 0.8*new_row['WEBSITE_VISITS']
            + 40*customer_service_lang_not_offered(new_row['HOME_LANGUAGE'])
            -70
            )
        lapse_prob = 1/(1+np.exp(-z))
        new_row['LAPSE_IN_12M'] = 1 if lapse_prob>0.5 else 0
        
        # Append new datapoint
        df = df._append(new_row, ignore_index=True)
    
    # Seperate customer survey and lapse data
    df_customer_survey = df[survey_cols]
    df_lapse_data = df.drop(survey_cols, axis=1).rename({'POL_NUMBER_2': 'POL_NUMBER',
                                                         'MONTH_KEY_2':'MONTH_KEY'
                                                         }, axis=1)

    return df_customer_survey, df_lapse_data










