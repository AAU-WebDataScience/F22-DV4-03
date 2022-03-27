# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 09:58:17 2022

@author: MarcusA
"""
import csv 
import pandas as pd

results = []
results2 = []
with open('country_cusine_list.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        results.append(row[0])

with open('distinct_no_specialchar.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        results2.append(row[0])



newList = []
for element in range(len(results2)):
    for row in range(len(results)):
        if results2[element] == results[row]:
            newList.append(str(results[row]))


df = pd.DataFrame(newList) 
    
#saving the dataframe 
df.to_csv('country_cusine_filtered_list.csv', index = False)