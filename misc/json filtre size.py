# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:21:05 2022

@author: MarcusA
"""

import json
import csv 

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD        

n = 0
data_user= []
with open('yelp_academic_dataset_user.json', encoding="utf8") as f:
    for line in f:
        if n > 1000:
            break
        data_user.append(json.loads(line))
        n = n + 1

json_user = json.dumps(data_user)
json_user = json.loads(json_user)

n = 0
jsonFile = open("yelp_academic_dataset_user_1000.json", "w")
for lines in json_user:
    jsonFile.write(json_user[n])
    n = n + 1
jsonFile.close()

n = 0
data_review= []
with open('yelp_academic_dataset_review.json', encoding="utf8") as f:
    for line in f:
        if n > 1000:
            break
        data_review.append(json.loads(line))
        n = n + 1
        
        
json_rewiew= json.dumps(data_review)
json_rewiew = json.loads(json_rewiew)

jsonFile = open("yelp_academic_dataset_review_10000", "w")
n = 0
for lines in json_user:
    jsonFile.write(data_review[n])
    n = n + 1
jsonFile.close()