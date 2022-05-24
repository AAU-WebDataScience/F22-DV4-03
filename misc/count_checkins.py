# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:15:01 2022

@author: storm
"""


import json
import pandas as pd
data_checkin = []
with open('D:/ONEDRIVE_FREE_FOLDER/Uni-Datavidenskab/YELP/yelp_academic_dataset_checkin.json', encoding="utf8") as f:
    for line in f:
        data_checkin.append(json.loads(line))
        
        

business_id_list = []
n = 0        
for i in data_checkin:
    business_id_list.append(data_checkin[n]['business_id'])
    n = n + 1

n = 0    
business_list = {}
for element in business_id_list:
    business_list[element] = data_checkin[n]['date'].count(',') + 1
    n = n + 1
    
df = pd.DataFrame(list(business_list.items()),columns = ['Business_Checkins','Amount'])

df_sorted = df.sort_values(by='Amount', ascending=False)

df_sorted.to_csv('amount_of_business_checkins.csv', index=False)