# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:32:31 2022

@author: storm
"""


import json
import csv 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_business = []

#10k lines - D:/Documents - HDD/GitHub/F22-DV4-03/Test for yelp datasets/yelp_academic_dataset_business_10000lines.json
#full data - D:/ONEDRIVE_FREE_FOLDER/Uni-Datavidenskab/YELP/yelp_academic_dataset_business.json


with open('D:/ONEDRIVE_FREE_FOLDER/Uni-Datavidenskab/YELP/yelp_academic_dataset_business.json', encoding="utf8") as f:
    for line in f:
        data_business.append(json.loads(line))
        
def string_seperate(string):
    n = 0
    cate_list = []
    a_list = string.split(", ")
    for element in a_list:
        cate_list.append(element)
    n = n +1
    return cate_list

state_dict_count = {"AL" : 0, "AK" : 0, "AZ" : 0, "AR" : 0, "CA" : 0, "CO" : 0, 
                    "CT" : 0, "DE" : 0, "DC" : 0, "FL" : 0, "GA" : 0, "HI" : 0, 
                    "ID" : 0, "IL" : 0, "IN" : 0, "IA" : 0, "KS" : 0, "KY" : 0,
                    "LA" : 0, "ME" : 0, "MD" : 0, "MA" : 0, "MI" : 0, "MN" : 0, 
                    "MS" : 0, "MO" : 0, "MT" : 0, "NE" : 0, "NV" : 0, "NH" : 0, 
                    "NJ" : 0, "NM" : 0, "NY" : 0, "NC" : 0, "ND" : 0, "OH" : 0, 
                    "OK" : 0, "OR" : 0, "PA" : 0, "PR" : 0, "RI" : 0, "SC" : 0, 
                    "SD" : 0, "TN" : 0, "TX" : 0, "UT" : 0, "VT" : 0, "VA" : 0, 
                    "VI" : 0, "WA" : 0, "WV" : 0, "WI" : 0, "WY" : 0
                    }


# def count_categories():
#     n = 0
#     for i in data_business:
#         if data_business[n]['categories'] != None:
#             catagory_list = string_seperate(data_business[n]['categories'])
#             for element in range(len(catagory_list)):
#                 mydict[element] + = 1
#         n = n + 1
#         if n % 1000 == 0:
#             print(n)
            
# count_cities()
n = 0
for i in data_business:
    state_dict_count[data_business[n]['state']] = state_dict_count.get(data_business[n]['state'], 0) + 1
    n = n + 1

df = pd.DataFrame(list(state_dict_count.items()),columns = ['State','Amount'])

df_sorted = df.sort_values(by='Amount', ascending=False)

#df_sorted.to_csv('amount_of_states.csv', index=False) 

plt.bar(
    height=df_sorted['Amount']
)