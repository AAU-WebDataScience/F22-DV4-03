# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 11:41:56 2022

@author: Johnnie
"""

import json
import csv 

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD

#list to save each 
data_user= []
n = 0
with open('yelp_academic_dataset_user.json', encoding="utf8") as f:
    for line in f:
        data_user.append(json.loads(line))

schema = Namespace("https://schema.org/")
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")

g = Graph()


for i in data_user[0:10]:
    if len(data_user[n]['name']) > 0 and data_user[n]['name'] != None:
        g.add((URIRef(yelp_user + data_user[n]['user_id']), schema.givenName, Literal(data_user[n]['name'])))
    if len(str(data_user[n]['review_count'])) > 0:
        g.add((URIRef(yelp_user + data_user[n]['user_id']), schema.reviewCount, Literal(data_user[n]['review_count'])))
        n = n + 1

#for s, p, o in g:
#    print(s+"     "+p+"     "+o)
    
g.serialize(format="xml", destination="user.xml")
