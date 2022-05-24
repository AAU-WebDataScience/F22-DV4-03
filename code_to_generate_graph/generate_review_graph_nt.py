# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:16:00 2022

@author: ramme
"""
import json

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
yelp_review_vc = Namespace("https://www.yelp.com/kg/review/votes_count/")

graph_file = open('review-yelp-kg.nt', 'a')

n = 0

rvw_votes_lst = ['useful', 'funny', 'cool']

with open('yelp_academic_dataset_review.json', encoding="utf8") as f:
    for line in f:
        line = line.encode("ascii", "ignore") #removing unicode characters
        line = json.loads(line) #reading in the line from the .json file
        g = Graph() #creating a graph
        #schema.orgitemReviewed
        if len(line['business_id']) > 0 and line['business_id'] != None:
            g.add((URIRef(yelp_user + line['user_id']), 
                   schema.itemReviewed, 
                   URIRef(yelp_business + line['business_id'])))
        #schema.org/author
        if len(line['review_id']) > 0 and line['review_id'] != None:
            g.add((URIRef(yelp_business + line['business_id'] + "?hrid=" + line['review_id']),
                   schema.author,
                   URIRef(yelp_user + line['user_id'])))
        #URI for a specific review: yelp_business + business_id + ?hrid= + review_id
        if line['stars'] != None:
            g.add((URIRef(yelp_business + line['business_id'] + "?hrid=" + line['review_id']), 
                   schema.starRating, 
                   Literal(line['stars'], datatype=XSD.int)))
        #Date of review:
        if line['date'] != None:
            g.add((URIRef(yelp_business + line['business_id'] + "?hrid=" + line['review_id']), 
                   schema.dateCreated, 
                   Literal(line['date'], datatype=XSD.dateTime)))
        #Which biz does a review review? schema.itemReviewed
        if line['review_id'] != None and line['business_id'] != None:
            g.add((URIRef(yelp_business + line['business_id'] + "?hrid=" + line['review_id']), 
                   schema.itemReviewed, 
                   URIRef(yelp_business + line['business_id'])))
        for j in rvw_votes_lst:
            if line[j] != None:
                g.add((URIRef(yelp_business + line['business_id']), 
                       URIRef(yelp_review_vc + j), 
                       Literal(line[j], datatype=XSD.int)))
        if line['business_id'] != None and line['text'] != None:
            g.add((URIRef(yelp_business + line['business_id'] + "?hrid=" + line['review_id']), 
                   schema.text, 
                   Literal(line['text'], datatype=XSD.string)))
        
        graph_file.write(g.serialize(format="nt")) #appending the triples to the graph file
        
        print(n) #counting the number of lines transformed to rdf (-1)
        
        n += 1
        
graph_file.close()