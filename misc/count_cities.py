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
postal_code_list = []
cities_postal_list = []
for i in data_business:
    if data_business[n]['state'] == "AB":
        cities_postal_list.append(str(data_business[n]['city']))
        cities_list.append(str((data_business[n]['city'])))
    else:
        cities_postal_list.append(str(data_business[n]['city'])+str(data_business[n]['postal_code']))
    n = n + 1

distinct_postal_code_list = list(set(postal_code_list))
distinct_cities_list = list(set(cities_list))
distinct_cities_postal_list = list(set(cities_postal_list))

# print("Lines in dataset: "+ str(n))
# print("Distinct cities: " + str(len(distinct_cities_list)))
# print("Distinct postal codes: "+ str(len(distinct_postal_code_list)))
print(distinct_cities_list)
print("-----------------------------------\n\n\n\n\n-------------------------------------------")
print(len(distinct_cities_list))
print(distinct_cities_postal_list)
print("distinct combinationes of city and postalcode: " + str(len(distinct_cities_postal_list)))
