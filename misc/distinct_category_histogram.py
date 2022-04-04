# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:13:54 2022

@author: MarcusA
"""

import json
import csv 
import pandas as pd

data_business = []

with open('yelp_academic_dataset_business_10000lines.json', encoding="utf8") as f:
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
        
def create_exist_list():
    df_exist_v1 = pd.read_csv('category_exist_in_db_List.csv')
    
    df_exist_v2 = pd.read_csv('category_exist_in_db_List_v2.csv')
    
    df_exist_v3 = pd.read_csv('category_exist_in_db_List_v3.csv')
    
    df_sp_exist_v1 = pd.read_csv('category_special_exist_v1.csv')
    
    exist_list = []
    
    for index, row in df_exist_v1.iterrows():
        exist_list.append(row[0])
        
    for index, row in df_exist_v2.iterrows():
        exist_list.append(row[0])
        
    for index, row in df_exist_v3.iterrows():
        exist_list.append(row[0])
        
    for index, row in df_sp_exist_v1.iterrows():
        exist_list.append(row[0])
    
    hist_data = pd.DataFrame(columns=['0'])
    
    print('done')




    n = 0
    for i in data_business:
        if data_business[n]['categories'] != None:
            catagory_list = string_seperate(data_business[n]['categories'])
            for item in range(len(exist_list)):
                for element in range(len(catagory_list)):
                    if catagory_list[element] == exist_list[item]:
                        hist_data = hist_data.append({'0':'1'}, ignore_index=True)
        print(n)
        n = n + 1

    hist_data.fillna('2', inplace=True)
    
    hist_data.to_csv('category_hist.csv', index = False)

create_exist_list()

hist_data = pd.read_csv('category_hist.csv')
print('done')

plot = hist_data.plot.pie(y='0', figsize=(5, 5))