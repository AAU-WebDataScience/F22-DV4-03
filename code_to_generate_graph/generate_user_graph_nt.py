# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:50:21 2022

@author: ramme
"""
import json 

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

#schema.org prefix
schema = Namespace("https://schema.org/")
#to map the users id:
yelp_user = Namespace("https://www.yelp.com/user_details?userid=")
#to map the number of useful, funny, cool, fans votes given by the user - object is int:
yelp_user_vc = Namespace("https://www.yelp.com/kg/user/votes_count/")
#to map the number of compliments received by a user - object is int:
yelp_user_cmplm = Namespace("https://www.yelp.com/kg/user/compliment_count/")
#to map the number average number of stars given by a user:
yelp_user_root = Namespace("https://www.yelp.com/kg/user/")

#Auxiliary functions
#--------------------
#Function to create a list from a string based on ',' - also used in graf_business.py
def string_seperate(string):
    n = 0
    friends_list = []
    a_list = string.split(", ")
    for element in a_list:
        friends_list.append(element)
    n += 1
    return friends_list

#To handle special case - 2020 in elite list has been split into 20, 20:
def string_seperate_elite(string):
    n = 0
    lst = []
    a_list = string.replace("20,20","2020")
    a_list = a_list.split(", ")
    for element in a_list:
        lst.append(element)
    n += 1
    return lst

#--------------------

graph_file = open('user-yelp-kg.nt', 'a')

n = 0

user_votes_lst = ['useful', 'funny', 'cool', 'fans']

cmplm_lst = ['compliment_hot', 'compliment_more', 'compliment_profile', 
             'compliment_cute', 'compliment_list', 'compliment_note', 
             'compliment_plain', 'compliment_cool', 'compliment_funny', 
             'compliment_writer', 'compliment_photos']

with open('yelp_academic_dataset_user.json', encoding="utf8") as f:
    for line in f:
        line = line.encode("ascii", "ignore") #removing unicode characters
        line = json.loads(line) #reading in the line from the .json file
        g = Graph() #creating a graph
        #creating triple with predicate schema.org/givenName
        if line['name'] != None:
            g.add((URIRef(yelp_user + line['user_id']), 
                   schema.givenName, 
                   Literal(line['name'], datatype=XSD.string)))
        #creating triple with predicate schema.org/reviewCount
        if line['review_count'] != None:
            g.add((URIRef(yelp_user + line['user_id']), 
                   schema.reviewCount, 
                   Literal(line['review_count'], datatype=XSD.int)))
        ##creating triple with predicate schema.org/startTime:
        if len(line['yelping_since']) > 0 and line['yelping_since'] != None:
            g.add((URIRef(yelp_user + line['user_id']), 
                   schema.startTime, 
                   Literal(line['yelping_since'], datatype=XSD.dateTime)))
        ##creating triple with predicate schema.org/knows:
        if line['friends'] != None:
            #split the string in categories to a list, create list as catagory_list
            friends_list = string_seperate(line['friends'])
            for elem in friends_list:
                g.add((URIRef(yelp_user + line['user_id']), 
                       schema.knows, 
                       URIRef(yelp_user + elem)))

        for j in user_votes_lst:
            if line[j] != None:
                g.add((URIRef(yelp_user + line['user_id']), 
                       URIRef(yelp_user_vc + j), 
                       Literal(line[j], datatype=XSD.int)))

        for j in cmplm_lst:
            if line[j] != None:
                attrb = j.split("_")[1]
                g.add((URIRef(yelp_user + line['user_id']), 
                       URIRef(yelp_user_cmplm + attrb), 
                       Literal(line[j], datatype=XSD.int)))

        if line['average_stars'] != None:
            g.add((URIRef(yelp_user + line['user_id']), 
                   URIRef(yelp_user_root + "average_stars"), 
                   Literal(line['average_stars'], datatype=XSD.float)))

        if line['elite'] != None:
            #split the elements (years) in 'elite' to create a list:
            yrs_list = string_seperate_elite(line['elite'])
            for elem in yrs_list:
                g.add((URIRef(yelp_user + line['user_id']), 
                       URIRef(yelp_user_root + "elite"), 
                       Literal(elem, datatype=XSD.year)))
        
        graph_file.write(g.serialize(format="nt")) #appending the triples to the graph file
        
        print(n) #counting the number of lines transformed to rdf (-1)
        
        n += 1
        
graph_file.close()

