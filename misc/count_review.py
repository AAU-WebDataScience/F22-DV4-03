# -*- coding: utf-8 -*-
"""
Created on Tue May 24 09:14:52 2022

@author: storm
"""

import json
import pandas as pd
data_review = []
with open('D:/ONEDRIVE_FREE_FOLDER/Uni-Datavidenskab/YELP/yelp_academic_dataset_review.json', encoding="utf8") as f:
    for line in f:
        data_review.append(json.loads(line))
        
        
        
###
#Count user reviews
###        
        
# user_id_list = []
# n = 0
# for i in data_review:
#     user_id_list.append(data_review[n]['user_id'])
#     n = n + 1

# user_list = {}
# for element in user_id_list:
#     user_list[element] = user_list.get(element, 0) + 1
    

# df = pd.DataFrame(list(user_list.items()),columns = ['User_reviews','Amount'])

# df_sorted = df.sort_values(by='Amount', ascending=False)

# df_sorted.to_csv('amount_of_user_reviews.csv', index=False) 

###
#Count business reviews
###        
        
business_id_list = []
n = 0
for i in data_review:
    business_id_list.append(data_review[n]['business_id'])
    n = n + 1

business_list = {}
for element in business_id_list:
    business_list[element] = business_list.get(element, 0) + 1
    

df = pd.DataFrame(list(business_list.items()),columns = ['Business_reviews','Amount'])

df_sorted = df.sort_values(by='Amount', ascending=False)

df_sorted.to_csv('amount_of_business_reviews.csv', index=False)