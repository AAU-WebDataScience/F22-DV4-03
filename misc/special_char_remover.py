# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:32:38 2022

@author: MarcusA
"""

import csv 
import pandas as pd
import re

df = pd.read_csv('distinct_category_list_1311.csv')

special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

n = 0

for row in df.iloc():
    if(special_char.search(row[0]) == None):
        print('String does not contain any special characters.')
        
    else:
        print(row + 'have a special_char')
        df = df.drop(labels=[n], axis=0)
    print(n)
    n = n + 1
    
    
    
df.to_csv('distinct_no_specialchar.csv', index = False)



'''
df2 = pd.read_csv('distinct_no_specialchar.csv')

list2 = df2.values.tolist()

n = 0
for element in list2:
    
    list2[n].lower()
    n = n +1

print(list2)
#http://dbpedia.org/resource/California
'''


