# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 13:34:45 2022

@author: Johnnie
"""

import json
import csv 

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD


#list to save each fragment
data_business = []
n = 0
#open json file line for line
#smaller size for original file yelp_academic_dataset_business_10000lines.json
#real file yelp_academic_dataset_business.json
with open('yelp_academic_dataset_business_10000lines.json', encoding="utf8") as f:
    for line in f:
        data_business.append(json.loads(line))

#predicator
schema = Namespace("https://schema.org/")
g = Graph()


#transform the list and append to Graph 

for i in data_business:
    if len(data_business[n]['name']) > 0 and data_business[n]['name'] != None:
        g.add((Literal(data_business[n]['business_id']), schema.legalName, Literal(data_business[n]['name'])))
    if len(data_business[n]['address']) > 0:
        g.add((Literal(data_business[n]['business_id']), schema.streetAddress, Literal(data_business[n]['address'])))
    
    #is all the data from the us?
    if len(data_business[n]['state']) > 0:
        g.add((Literal(data_business[n]['business_id']), schema.addressRegion, Literal(data_business[n]['state'])))
    if len(data_business[n]['postal_code']) > 0:
        g.add((Literal(data_business[n]['business_id']), schema.postalCode, Literal(data_business[n]['postal_code'])))
    
    #the len does not apply for doubles or int
    if len(str(data_business[n]['latitude'])) > 0:
        g.add((Literal(data_business[n]['business_id']), schema.latitude, Literal(data_business[n]['latitude'])))
    if len(str(data_business[n]['longitude'])) > 0:
        g.add((Literal(data_business[n]['business_id']), schema.longitude, Literal(data_business[n]['longitude'])))
    if len(str(data_business[n]['stars'])) > 0:
        g.add((Literal(data_business[n]['business_id']), schema.starRating, Literal(data_business[n]['stars'])))
    n = n + 1
    #these 2 line have have problems with predicate 
    #g.add((Literal(data[n]['business_id']), schema.ratingCount, Literal(data[n]['ratingCount'])))
    #g.add((Literal(data[n]['business_id']), schema.brand, Literal(data[n]['categories'])))
    
    
#print 3 variabel for graph in g
for s, p, o in g:
    print(s+"     "+p+"     "+o)
    
    