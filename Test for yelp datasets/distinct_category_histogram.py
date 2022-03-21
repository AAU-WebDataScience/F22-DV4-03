# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:13:54 2022

@author: MarcusA
"""

import json
import csv 
import pandas as pd

data_business = []

with open('yelp_academic_dataset_business.json', encoding="utf8") as f:
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


#count distinct catagories in data_business
final_list = []
for element in range(len(data_business)):
    if data_business[element]['categories'] != None:
        distinct_list = string_seperate(data_business[element]['categories'])
        final_list.append(distinct_list)

#create flat list out of nested list
flat_list = [item for sublist in final_list for item in sublist]

df = pd.DataFrame(flat_list)

df_2 = df.value_counts()

'''
df_2.to_csv('distinct_value_counts.csv')

hist = df_2.plot.bar()
'''

hist2 = df_2.iloc[0:100].plot.bar(x = 0)

hist3 = df_2.iloc[0:10].plot.bar(x = 0)


'''
df = pd.read_csv('distinct_value_counts.csv', header=None)
hist = df.plot.bar()

hist2 = df.iloc[0:100].plot.bar()

hist2 = df.iloc[0:10].plot.bar(x = 0)
'''