# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:17:50 2022

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
        





# def string_seperate(string):
#     n = 0
#     cate_list = []
#     a_list = string.split(", ")
#     for element in a_list:
#         cate_list.append(element)
#     n = n +1
#     return cate_list



#Counts how many of each attribute that exists
# mydict = {}
# n = 0
# attribute_list = []
# value_list = []   
# for i in data_business:
#     if data_business[n]['attributes'] != None:
#         keys, values = zip(*data_business[n]['attributes'].items())
#         for element in keys:
#             mydict[element] = mydict.get(element, 0) + 1
#     n = n + 1
#     if n % 1000 == 0:
#         print(n)  

# print(mydict)
# df = pd.DataFrame(list(mydict.items()),columns = ['Attribute','Amount'])

# df_sorted = df.sort_values(by='Amount', ascending=False)

# df_sorted.to_csv('amount_of_attributes.csv', index=False) 


       
# n = 0
# big_string = ""
# for i in data_business:
#     if data_business[n]['attributes'] != None:
#         big_string = big_string + str(data_business[n]['attributes'])   
#     n = n + 1
#     if n % 1000 == 0:
#         print(n)  

# print(big_string)



#Counts how many of each attribute that exists
mydict = {}
n = 0
attribute_list = []
value_list = []   
for i in data_business:
    try:
        values = data_business[n]['attributes']['ByAppointmentOnly']
        mydict[values] = mydict.get(values, 0) + 1
        n = n + 1
        if n % 1000 == 0:
            print(n)
    except:
        n = n + 1
        if n % 1000 == 0:
            print(n)
        

        
print(mydict)