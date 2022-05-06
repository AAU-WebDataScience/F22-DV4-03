# -*- coding: utf-8 -*-
"""
Created on Fri May  6 09:47:28 2022

@author: ramme
"""

import json 

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

#list to save the data for each user
data_checkin = []

#populating the list
with open('yelp_academic_dataset_checkin.json', encoding="utf8") as f:
    for line in f:
        data_checkin.append(json.loads(line))

#schema.org prefix
schema = Namespace("https://schema.org/")
#To create biz URI:
yelp_business = Namespace("https://www.yelp.com/biz/")

g = Graph()

#Auxiliary functions
#--------------------
#Function to create a list from a string based on ',' - also used in graf_business.py and generate_user_graph.py
def string_seperate(string):
    n = 0
    friends_list = []
    a_list = string.split(", ")
    for element in a_list:
        friends_list.append(element)
    n += 1
    return friends_list

#--------------------

def checkin_dates_rdf():
    for n in range(len(data_checkin)):
        if data_checkin[n]['date'] != None:
            #split the elements (dates) in 'date' to create a list:
            dates_list = string_seperate(data_checkin[n]['date'])
            for elem in dates_list:
                g.add((URIRef(yelp_business + data_checkin[n]['business_id']), 
                       schema.startTime, 
                       Literal(elem, datatype=XSD.dateTime)))

checkin_dates_rdf()

#change this:
g.serialize(format="xml", destination="checkin_graph.xml")