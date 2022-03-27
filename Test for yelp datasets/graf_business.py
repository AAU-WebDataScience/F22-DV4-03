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
cuisineList = []
existdbList = []
noexistdbList = []

#open json file line for line
#smaller size for original file yelp_academic_dataset_business_10000lines.json
#real file yelp_academic_dataset_business.json
with open('yelp_academic_dataset_business.json', encoding="utf8") as f:
    for line in f:
        data_business.append(json.loads(line))
df = pd.read_csv('csvData.csv')

with open('country_cusine_filtered_list.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        cuisineList.append(row[0])
        
with open('distinct_no_specialchar.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        existdbList.append(row[0])
        
with open('distinct_with_specialchar.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        noexistdbList.append(row[0])

def string_seperate(string):
    n = 0
    cate_list = []
    a_list = string.split(", ")
    for element in a_list:
        cate_list.append(element)
    n = n +1
    return cate_list

def code_to_state(code):
    n = 0
    for index, row in df.iterrows():
        if str(code) == str(df.loc[n,'Code']):
            return str(df.loc[n,'State'])
        #str(df.loc[n,])
        n = n + 1
        

def change_format_to_db(catagory):
    #this function takes a string in catagory from yelp
    #and gives the correct format to put in dbpedia
    
    #Everthing in string to lowercase
    newcatagory = catagory.lower()
    
    #capitalize first letter 
    newcatagory = catagory.capitalize()
    
    #replace empty with _
    newcatagory = catagory.replace(" ", "_")
    
    return newcatagory

#predicator
schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
db_state = Namespace("http://dbpedia.org/resource/")
g_maps = Namespace("https://maps.google.com/?q=")

g = Graph()


def triple_maker_name():
    #for each name that exist for a business, add a triple to the graph
    n = 0
    for i in data_business:
        if len(data_business[n]['name']) > 0 and data_business[n]['name'] != None:
            #append to graph
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.legalName, Literal(data_business[n]['name'])))
        n = n + 1
    print('name done')

def triple_maker_address():
    #for each address that exist for a business, add a triple to the graph
    n = 0
    for i in data_business:
        #append to graph
        if len(data_business[n]['address']) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.streetAddress, Literal(data_business[n]['address'])))
        n = n + 1
    print('address done')
        
def triple_maker_state():
    n = 0
    for i in data_business:
        #append to graph
        if len(data_business[n]['state']) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.addressRegion, URIRef(db_state + str(code_to_state(data_business[n]['state'])))))
        n = n + 1
        
    print('state done')
        
def triple_maker_postal():
    n = 0
    for i in data_business:
        #append to graph
        if len(data_business[n]['postal_code']) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.postalCode, Literal(data_business[n]['postal_code'])))
        n = n + 1
        
    print('postal done')

def triple_maker_latlong():
    n = 0
    for i in data_business:
        #append to graph
        if len(str(data_business[n]['latitude'])) > 0 and len(str(data_business[n]['longitude'])) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.geo, URIRef(g_maps + str(data_business[n]['latitude'])) + ',' + str(data_business[n]['longitude'])))
        n = n + 1
        
    print('lat+long done')
        
def triple_maker_stars():
    n = 0
    for i in data_business:
        #append to graph
        if len(str(data_business[n]['stars'])) > 0:
            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.starRating, Literal(data_business[n]['stars'])))
        n = n + 1
    print('stars done')
        
def triple_maker_cg_cuisine():
    for n in range(len(data_business)):
        if data_business[n]['categories'] != None:
            #split the string in categories to a list, create list as catagory_list
            catagory_list = string_seperate(data_business[n]['categories'])
                
            #for every item in catagory_list, compare it with the cuisineList
            for item in range(len(cuisineList)):
                for element in range(len(catagory_list)):
                    #the item in category exist, add it to the graph
                    if catagory_list[element] == cuisineList[item]:
                        #cause the cuisines exist as country+_cuisine in dbpedia
                        #so every country get added a _cuisine after
                        g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.category, URIRef(db_state + str(cuisineList[element])+ str('_cuisine'))))
    print('category for cuisine done')

def triple_maker_cg_in_db_exist():
    for n in range(len(data_business)):
        if data_business[n]['categories'] != None:
            #split the string in categories to a list, create list as catagory_list
            catagory_list = string_seperate(data_business[n]['categories'])
                
            #for every item in catagory_list, compare it with the cuisineList
            item1 = 0
            for item in range(len(catagory_list)):
                element1 = 0
                for element in range(len(existdbList)):
                    #the item in category exist, add it to the graph
                    if str(catagory_list[item]) == str(existdbList[element]):
                        #the format in dbpedia is first letter is upper case
                        #and the rest of the letters are lowercase
                        #so every string goes through the function change_format_to_db
                        #in order to be the correct format
                        g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.category, URIRef(db_state + change_format_to_db(existdbList[element]))))
    print('category that exist in db done')
        
   
def triple_maker_cg_in_db_not_exist():
    
    # this function is not functioning
    n = 0
    for i in data_business:
        if data_business[n]['categories'] != None:
            #split the string in categories to a list, create list as catagory_list
            for element in range(len(data_business[n]['categories'])):
                catagory_list = string_seperate(data_business[element]['categories'])
                #for every item in catagory_list, compare it with the cuisineList
                for item in range(len(noexistdbList)):
                    for element in range(len(catagory_list)):
                        if catagory_list[element] == noexistdbList[item]:
                            g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.category, Literal(noexistdbList[element])))
        n = n + 1


def print_triple():    
    #print 3 variabel for graph in g
    for s, p, o in g:
        print(s+'  '+p+'  '+o)

        #code_to_state('CA')
    #http://dbpedia.org/resource/United_States
    #https://dbpedia.org/page/California 
    #http://dbpedia.org/resource/California
    
triple_maker_name()
triple_maker_address()
triple_maker_state()
triple_maker_postal()
triple_maker_latlong()
triple_maker_stars()
triple_maker_cg_cuisine()
triple_maker_cg_in_db_exist()
g.serialize(destination="Business_v1.ttl")
print('done')

'''
       
df = pd.DataFrame(final_list) 
    
#saving the dataframe 
df.to_csv('distinct_category_list.csv', index = False)
print(string_seperate(data_business[9]['categories']))

g.add((URIRef(yelp_business + data_business[n]['business_id']), schema.starRating, Literal(data_business[n]['stars'])))

    
if __name__ == "__main__":
    triple_maker()
    g.serialize(format="xml", destination="business.xml")
'''
