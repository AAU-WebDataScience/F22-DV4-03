# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:16:00 2022

@author: ramme
"""
import json

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

data_review = []

with open('yelp_academic_dataset_review.json', encoding="utf8") as f:
    for line in f:
        data_review.append(json.loads(line))

schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
yelp_review_vc = Namespace("https://www.yelp.com/kg/review/votes_count/")

g = Graph()

def user_to_busi_rdf(): #schema.itemReviewed
    n = 0
    for i in data_review:
        if len(data_review[n]['business_id']) > 0 and data_review[n]['business_id'] != None:
            g.add((URIRef(yelp_user + data_review[n]['user_id']), 
                   schema.itemReviewed, 
                   URIRef(yelp_business + data_review[n]['business_id'])))
        n += 1

def user_author_rvw_rdf(): #schema.author
    n = 0
    for i in data_review:
        if len(data_review[n]['review_id']) > 0 and data_review[n]['review_id'] != None:
            g.add((URIRef(yelp_user + data_review[n]['user_id']), 
                   schema.author, 
                   Literal(data_review[n]['review_id'])))
        n += 1

def rvw_num_stars_rdf(): #URI for a specific review: yelp_business + business_id + ?hrid= + review_id
    n = 0
    for i in data_review:
        if data_review[n]['stars'] != None:
            g.add((URIRef(yelp_business + data_review[n]['business_id'] + "?hrid=" + data_review[n]['review_id']), 
                   schema.starRating, 
                   Literal(data_review[n]['stars'], datatype=XSD.int)))
        n += 1

def date_rvw_created_rdf(): #Date of review
    n = 0
    for i in data_review:
        if data_review[n]['date'] != None:
            g.add((URIRef(yelp_business + data_review[n]['business_id'] + "?hrid=" + data_review[n]['review_id']), 
                   schema.dateCreated, 
                   Literal(data_review[n]['date'], datatype=XSD.dateTime)))
        n += 1

def rvw_rvw_of_biz_rdf(): #Which biz does a review review? schema.itemReviewed
    n = 0
    for i in data_review:
        if data_review[n]['review_id'] != None and data_review[n]['business_id'] != None:
            g.add((URIRef(yelp_business + data_review[n]['business_id'] + "?hrid=" + data_review[n]['review_id']), 
                   schema.itemReviewed, 
                   URIRef(yelp_business + data_review[n]['business_id'])))
        n += 1

def votes_rcvd_rdf(lst): #using a custom property URI for the relation ('useful', 'funny', 'cool') - subject is a biz, object is a count 
    n = 0
    for i in data_review:
        for j in lst:
            if data_review[n][j] != None:
                g.add((URIRef(yelp_business + data_review[n]['business_id']), 
                       URIRef(yelp_review_vc + j), 
                       Literal(data_review[n][j], datatype=XSD.int)))
        n += 1

#List to loop through by votes_rsvd_rdf:
rvw_votes_lst = ['useful', 'funny', 'cool']


def rvw_txt_rdf(): #Text content of review? schema.text
    n = 0
    for i in data_review:
        if data_review[n]['business_id'] != None and data_review[n]['text'] != None:
            g.add((URIRef(yelp_business + data_review[n]['business_id'] + "?hrid=" + data_review[n]['review_id']), 
                   schema.text, 
                   Literal(data_review[n]['text'])))
        n += 1

user_to_busi_rdf()
user_author_rvw_rdf()
rvw_num_stars_rdf()
date_rvw_created_rdf()
rvw_rvw_of_biz_rdf()
votes_rcvd_rdf(rvw_votes_lst)
rvw_txt_rdf()

g.serialize(format="xml", destination="review.xml")