# -*- coding: utf-8 -*-
"""
Created on Fri May  6 09:47:28 2022

@author: ramme
"""

import json 

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

#schema.org prefix
schema = Namespace("https://schema.org/")
#To create biz URI:
yelp_business = Namespace("https://www.yelp.com/biz/")

graph_file = open('checkin-yelp-kg.nt', 'a')

n = 0

#Auxiliary functions
#--------------------
#Function to create a list from a string based on ','
def string_seperate(string):
    n = 0
    friends_list = []
    a_list = string.split(", ")
    for element in a_list:
        friends_list.append(element)
    n += 1
    return friends_list

#--------------------

with open('yelp_academic_dataset_checkin.json', encoding="utf8") as f:
    for line in f:
        line = line.encode("ascii", "ignore") #removing any unicode characters
        line = json.loads(line) #reading in the line from the .json file
        g = Graph() #creating a graph
        if line['date'] != None:
            #split the elements (dates) in 'date' to create a list:
            dates_list = string_seperate(line['date'])
            for elem in dates_list:
                g.add((URIRef(yelp_business + line['business_id']), 
                       schema.startTime, 
                       Literal(elem, datatype=XSD.dateTime)))
        
        graph_file.write(g.serialize(format="nt")) #appending the triples to the graph file
        
        print(n) #counting the number of lines transformed to rdf (-1)
        
        n += 1
        
graph_file.close()