# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 13:34:45 2022

@author: Johnnie
"""

import json
import csv 
import pandas as pd

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD


#list to save each fragment
data_business = []
csvfile = []

#open json file line for line
#smaller size for original file yelp_academic_dataset_business_10000lines.json
#real file yelp_academic_dataset_business.json
with open('yelp_academic_dataset_business.json', encoding="utf8") as f:
    for line in f:
        data_business.append(json.loads(line))
df = pd.read_csv('csvData.csv')

def code_to_state(code):
    n = 0
    for index, row in df.iterrows():
        if str(code) == str(df.loc[n,'Code']):
            return str(df.loc[n,'State'])
        #str(df.loc[n,])
        n = n + 1

#predicator
schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
db_state = Namespace("http://dbpedia.org/resource/")

g = Graph()
final_list = []

def list_distinct(new_list):
    for element in new_list:
        final_list.append(distinct.element)

#transform the list and append to Graph 

def triple_maker():
    n = 0
    for i in data_business:
        if len(data_business[n]['name']) > 0 and data_business[n]['name'] != None:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.legalName, Literal(data_business[n]['name'])))
        if len(data_business[n]['address']) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.streetAddress, Literal(data_business[n]['address'])))
        
        #is all the data from the us?
        if len(data_business[n]['state']) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.addressRegion, URIRef(db_state + str(code_to_state(data_business[n]['state'])))))
        if len(data_business[n]['postal_code']) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.postalCode, Literal(data_business[n]['postal_code'])))
        
        #the len does not apply for doubles or int
        if len(str(data_business[n]['latitude'])) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.latitude, Literal(data_business[n]['latitude'])))
        if len(str(data_business[n]['longitude'])) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.longitude, Literal(data_business[n]['longitude'])))
        if len(str(data_business[n]['stars'])) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.starRating, Literal(data_business[n]['stars'])))
        n = n + 1
        #these 2 line have have problems with predicate 
        #g.add((Literal(data[n]['business_id']), schema.ratingCount, Literal(data[n]['ratingCount'])))
        #g.add((Literal(data[n]['business_id']), schema.brand, Literal(data[n]['categories'])))
    
def print_triple():    
    #print 3 variabel for graph in g
    for s, p, o in g:
        print(s+'  '+p+'  '+o)

        #code_to_state('CA')
    #http://dbpedia.org/resource/United_States
    #https://dbpedia.org/page/California 
    #http://dbpedia.org/resource/California

def string_seperate():
    n = 0
    for element in range(len(data_business)):
        if data_business[n]['categories'] != None:
            string = data_business[n]['categories']
            a_list = string.split(", ")
            for element in a_list:
                if element not in final_list:
                    final_list.append(element)
        n = n + 1
        
string_seperate()

# importing pandas as pd  
import pandas as pd  
       
df = pd.DataFrame(final_list) 
    
# saving the dataframe 
df.to_csv('distinct_category_list.csv', index = False)
#print(string_seperate(data_business[9]['categories']))

#g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.starRating, Literal(data_business[n]['stars'])))

    
#if __name__ == "__main__":
#    triple_maker()
#    g.serialize(format="xml", destination="business.xml")
    