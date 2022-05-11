# -*- coding: utf-8 -*-
"""
Created on Fri May  6 10:37:44 2022

@author: ramme
"""
import json 

from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import XSD
import gc
import time

#schema.org prefix
schema = Namespace("https://schema.org/")
#to map the users id:
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
#to map the biz
yelp_business = Namespace("https://www.yelp.com/biz/")
#custom URI - used for predicate 'number of compliments'
yelp_tip = Namespace("https://www.yelp.com/kg/tip/")

n = 0

with open('yelp_academic_dataset_tip.json', encoding="utf8") as f:
    for line in f:
        line = json.loads(line)
        bn = BNode(n)
        g = Graph()
        
        if line["user_id"] != None:
            g.add((URIRef(yelp_user + line['user_id']),
                   schema.author, 
                   bn))
        if line['business_id'] != None:
            g.add((bn, 
                   schema.about, 
                   URIRef(yelp_business + line['business_id'])))
        if line['date'] != None:
            g.add((bn, 
                   schema.dateCreated, 
                   Literal(line['date'], datatype=XSD.dateTime)))
        if line['compliment_count'] != None: #This also generates objects where the count = 0
            g.add((bn, 
                   URIRef(yelp_tip + "compliment_count"), 
                   Literal(line['compliment_count'], datatype=XSD.int)))
        if line['text'] != None: #This also generates objects where the count = 0
            g.add((bn, 
                   schema.text, 
                   Literal(line['text'], datatype=XSD.string)))
        
        graph_text = open('user.txt', 'a')
        
        for s, p, o in g:
            graph_text.write(s+'  '+p+'  '+o + '\n')
        graph_text.close()
        gc.collect()
        
        n = n + 1
        
        print(n)
        
