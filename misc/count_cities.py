# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:52:22 2022

@author: storm
"""

import json
import csv 
import pandas as pd

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
cities_list = []
for i in data_business:
    cities_list.append(data_business[n]['city'])
    n = n + 1

print(cities_list)
print(len(cities_list))
distinct_cities_list = list(set(cities_list))

#print(distinct_cities_list)
print("length of dataset: " + str(len(data_business)))

print(len(distinct_cities_list))
