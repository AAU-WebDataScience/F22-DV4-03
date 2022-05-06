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
    for i in data_tip:
        if len(data_tip[n]['text']) > 0 and data_tip[n]['user_id'] != None:
            g.add((BNode(data_tip[n]['text']), 
                   schema.author, 
                   URIRef(yelp_user + data_tip[n]['user_id'])))
        n += 1
         
def tip_about_biz_rdf(): #schema.about
    n = 0
    for i in data_tip:
        if len(data_tip[n]['text']) > 0 and data_tip[n]['business_id'] != None:
            g.add((BNode(data_tip[n]['text']), 
                   schema.about, 
                   URIRef(yelp_business + data_tip[n]['business_id'])))
        n += 1

def date_tip_created_rdf(): #Date of tip
    n = 0
    for i in data_tip:
        if len(data_tip[n]['text']) > 0 and data_tip[n]['date'] != None:
            g.add((BNode(data_tip[n]['text']), 
                   schema.dateCreated, 
                   Literal(data_tip[n]['date'], datatype=XSD.dateTime)))
        n += 1

def tip_cmplm_count_rdf(): #Num of compliments received by a tip
    n = 0
    for i in data_tip[:50]:
        if len(data_tip[n]['text']) > 0 and data_tip[n]['compliment_count'] != None: #This also generates objects where the count = 0
            g.add((BNode(data_tip[n]['text']), 
                   URIRef(yelp_tip + "compliment_count"), 
                   Literal(data_tip[n]['compliment_count'], datatype=XSD.int)))
        n += 1

tip_author_rdf()
tip_about_biz_rdf()
date_tip_created_rdf()
tip_cmplm_count_rdf()

#change this:
g.serialize(format="xml", destination="tip_graph.xml")
