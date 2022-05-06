# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:30:41 2022

@author: storm
"""


import json
import csv 
import pandas as pd

data_business = []

with open('C:/Users/pmplo/OneDrive/Skrivebord/Yelp data/yelp_academic_dataset_business.json', encoding="utf8") as f:
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
            



with open('C:/Users/pmplo/OneDrive/Dokumenter/F22-DV4-03/Test for yelp datasets/distinct_category_list_1311.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('coors_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        mydict = {rows[0]:0 for rows in reader}
        
# count_categories()
n = 0
for i in data_business:
    if data_business[n]['categories'] != None:
        catagory_list = string_seperate(data_business[n]['categories'])
        for element in catagory_list:
            mydict[element] = mydict.get(element, 0) + 1
    n = n + 1
    if n % 1000 == 0:
        print(n)        

df = pd.DataFrame(list(mydict.items()),columns = ['Category','Amount'])

df_sorted = df.sort_values(by='Amount', ascending=False)

df_sorted.to_csv('amount_of_categories.csv', index=False) 
