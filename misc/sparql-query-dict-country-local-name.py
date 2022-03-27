# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:26:56 2022

@author: ramme
"""
from SPARQLWrapper import SPARQLWrapper2
import re

sparql = SPARQLWrapper2("http://dbpedia.org/sparql")

sparql.setQuery("""
    SELECT ?isValueOf
WHERE {
  { ?isValueOf ?property <http://dbpedia.org/resource/Category:Cuisine_by_country> }
}
""")

lst = []

for result in sparql.query().bindings:
    lst.append(result['isValueOf'].value)

lst_local = [] #in which to place the right local name: ...Category:XYZ_Cuisine

for ctry in lst:
    try:
        c = re.search('rce/(.*)', ctry) #getting rid of everthing up to 
                                        #'resource/'
        lst_local.append(c.group(1))
    except AttributeError:
        c = re.search('rce/(.*)', ctry)

ctry_lst = [] #in which to place only country names

for ctry in lst:
    try:
        c = re.search('y:(.*)_', ctry)
        ctry_lst.append(c.group(1))
    except AttributeError:
        c = re.search('y:(.*)_', ctry)

#creating dictionary based on two lists
dict_ctry_to_dbped_local_name = {ctry_lst[i]: lst_local[i] for i in range(len(ctry_lst))}

print(ctry_lst)

import csv 
import pandas as pd


df = pd.DataFrame(ctry_lst) 
df.to_csv('country_cusine_list.csv', index = None)






