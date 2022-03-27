# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 12:32:06 2022

@author: Johnnie
"""

import json
import csv 

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD

data_review= []
n = 0
with open('yelp_academic_dataset_review.json', encoding="utf8") as f:
    for line in f:
        data_review.append(json.loads(line))

schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
g = Graph()

for i in data_review[0:100]:
    if len(data_review[n]['business_id']) > 0 and data_review[n]['business_id'] != None:
        g.add((URIRef(yelp_user + data_review[n]['user_id']), schema.itemReviewed, URIRef(yelp_business + data_review[n]['business_id'])))
    if len(data_review[n]['review_id']) > 0 and data_review[n]['review_id'] != None:
        g.add((URIRef(yelp_user + data_review[n]['user_id']), schema.author, Literal(data_review[n]['review_id'])))
    if len(str(data_review[n]['stars'])) > 0 and data_review[n]['stars'] != None:
        g.add((Literal(data_review[n]['review_id']), schema.starRating, Literal(data_review[n]['stars'])))
    n = n +1
    
for s, p, o in g:
    print(s+"     "+p+"     "+o)

#https://www.yelp.com/biz/the-twisted-tandoor-tucson?hrid=2cA2JLrRw95epwACvsm0oQ&utm_campaign=header&utm_medium=embedded_review
    
#g.serialize(format="xml", destination="review.xml")