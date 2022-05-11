# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:12:13 2022

@author: ramme
"""

import json 

from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import XSD

#schema.org prefix
schema = Namespace("https://schema.org/")
#to map the user's id:
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
#to map the biz
yelp_business = Namespace("https://www.yelp.com/biz/")
#custom URI - used for predicate 'number of compliments'
yelp_tip = Namespace("https://www.yelp.com/kg/tip/")

graph_file = open('tip-yelp-kg.nt', 'a')

n = 0

with open('yelp_academic_dataset_tip.json', encoding="utf8") as f:
    for line in f:
        line = line.encode("ascii", "ignore") #removing unicode characters
        line = json.loads(line) #reading in the line from the .json file
        bn = BNode(n) #creating a blank node
        g = Graph() #creating a graph
        if line["user_id"] != None: #a user is the author of the tip
            g.add((URIRef(yelp_user + line['user_id']),
                   schema.author, 
                   bn))
        if line['business_id'] != None: #the tip is about some biz
            g.add((bn, 
                   schema.about, 
                   URIRef(yelp_business + line['business_id'])))
        if line['date'] != None: #the tip was created at a date
            g.add((bn, 
                   schema.dateCreated, 
                   Literal(line['date'], datatype=XSD.dateTime)))
        if line['compliment_count'] != None: #the tip has received # compliments
            g.add((bn, 
                   URIRef(yelp_tip + "compliment_count"), 
                   Literal(line['compliment_count'], datatype=XSD.int)))
        if line['text'] != None: #the tip has a text
            g.add((bn, 
                   schema.text, 
                   Literal(line['text'], datatype=XSD.string)))
        
        graph_file.write(g.serialize(format="nt")) #appending the triples to the graph file
        
        print(n) #counting the number of lines transformed to rdf (-1)
        
        n += 1
        
graph_file.close()
