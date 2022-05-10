# -*- coding: utf-8 -*-
"""
Created on Fri May  6 10:37:44 2022

@author: ramme
"""
import json 

from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import XSD

#list to save the data for each checkin
data_tip = []

#populating the list
with open('yelp_academic_dataset_tip.json', encoding="utf8") as f:
    for line in f:
        data_tip.append(json.loads(line))

#schema.org prefix
schema = Namespace("https://schema.org/")
#to map the users id:
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
#to map the biz
yelp_business = Namespace("https://www.yelp.com/biz/")
#custom URI - used for predicate 'number of compliments'
yelp_tip = Namespace("https://www.yelp.com/kg/tip/")

g = Graph()

def tip_author_rdf(): #schema.author
    n = 0
    for i in data_tip[:10]:
        bn = BNode(n)
        if data_tip[n]['user_id'] != None:
            g.add((URIRef(yelp_user + data_tip[n]['user_id']),
                   schema.author, 
                   bn))
        if data_tip[n]['business_id'] != None:
            g.add((bn, 
                   schema.about, 
                   URIRef(yelp_business + data_tip[n]['business_id'])))
        if data_tip[n]['date'] != None:
            g.add((bn, 
                   schema.dateCreated, 
                   Literal(data_tip[n]['date'], datatype=XSD.dateTime)))
        if data_tip[n]['compliment_count'] != None: #This also generates objects where the count = 0
            g.add((bn, 
                   URIRef(yelp_tip + "compliment_count"), 
                   Literal(data_tip[n]['compliment_count'], datatype=XSD.int)))
        if data_tip[n]['text'] != None: #This also generates objects where the count = 0
            g.add((bn, 
                   schema.text, 
                   Literal(data_tip[n]['text'], datatype=XSD.string)))
        n += 1

tip_author_rdf()

#change this:
g.serialize(format="xml", destination="tip_graph.xml")
