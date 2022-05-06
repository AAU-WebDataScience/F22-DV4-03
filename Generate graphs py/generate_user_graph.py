# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:50:21 2022

@author: ramme
"""
import json 

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

#list to save the data for each user
data_user = []

#populating the list
with open('yelp_academic_dataset_user.json', encoding="utf8") as f:
    for line in f:
        data_user.append(json.loads(line))

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

g = Graph()

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

def given_name_rdf():
    n = 0
    for i in data_user:
        if len(data_user[n]['name']) > 0 and data_user[n]['name'] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   schema.givenName, 
                   Literal(data_user[n]['name'], datatype=XSD.string)))
        n += 1

def revw_count_rdf():
    n = 0
    for i in data_user:
        if len(str(data_user[n]['review_count'])) > 0:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   schema.reviewCount, 
                   Literal(data_user[n]['review_count'], datatype=XSD.int)))
        n += 1

def yelping_since_rdf(): #mapping to https://schema.org/RegisterAction --> startTime
    n = 0
    for i in data_user:
        if len(data_user[n]['yelping_since']) > 0 and data_user[n]['yelping_since'] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   schema.startTime, 
                   Literal(data_user[n]['yelping_since'], datatype=XSD.dateTime)))
        n += 1

def friends_rdf(): #mapping to https://schema.org/Person --> knows
    for n in range(len(data_user)):
    #for n in range(len(data_user[:2])): #TO TEST THE FUNCTION
        if data_user[n]['friends'] != None:
            #split the string in categories to a list, create list as catagory_list
            friends_list = string_seperate(data_user[n]['friends'])
            for elem in friends_list:
                g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                       schema.knows, 
                       URIRef(yelp_user + elem)))
                
def useful_votes_gvn_rdf(): #using a custom property URI
    n = 0
    for i in data_user:
        if data_user[n]["useful"] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   URIRef(yelp_user_vc + "useful"), 
                   Literal(data_user[n]["useful"], datatype=XSD.int)))
        n += 1

def funny_votes_gvn_rdf(): #using a custom property URI
    n = 0
    for i in data_user:
        if data_user[n]["funny"] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   URIRef(yelp_user_vc + "funny"), 
                   Literal(data_user[n]["funny"], datatype=XSD.int)))
        n += 1

def cool_votes_gvn_rdf(): #using a custom property URI
    n = 0
    for i in data_user:
        if data_user[n]["cool"] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   URIRef(yelp_user_vc + "cool"), 
                   Literal(data_user[n]["cool"], datatype=XSD.int)))
        n += 1

def fans_votes_rcvd_rdf(): #using a custom property URI
    n = 0
    for i in data_user:
        if data_user[n]["fans"] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   URIRef(yelp_user_vc + "fans"), 
                   Literal(data_user[n]["fans"], datatype=XSD.int)))
        n += 1

def cmplm_rcvd_rdf(lst): #using a custom property URI
    n = 0
    for i in data_user:
        for j in lst:
            if data_user[n][j] != None:
                attrb = j.split("_")[1]
                g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                       URIRef(yelp_user_cmplm + attrb), 
                       Literal(data_user[n][j], datatype=XSD.int)))
        n += 1

#list to loop through by cmplm_rcvd_rdf(lst)
cmplm_lst = ['compliment_hot', 'compliment_more', 'compliment_profile', 
             'compliment_cute', 'compliment_list', 'compliment_note', 
             'compliment_plain', 'compliment_cool', 'compliment_funny', 
             'compliment_writer', 'compliment_photos']

def avg_stars_gvn_rdf(): #'average_stars': float, average rating of all reviews
    n = 0
    for i in data_user:
        if data_user[n]['average_stars'] != None:
            g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                   URIRef(yelp_user_root + "average_stars"), 
                   Literal(data_user[n]['average_stars'], datatype=XSD.float)))
        n += 1

def years_w_elite_status_rdf(): #using a custom property URI
    for n in range(len(data_user)):
        if data_user[n]['elite'] != None:
            #split the elements (years) in 'elite' to create a list:
            yrs_list = string_seperate_elite(data_user[n]['elite'])
            for elem in yrs_list:
                g.add((URIRef(yelp_user + data_user[n]['user_id']), 
                       URIRef(yelp_user_root + "elite"), 
                       Literal(elem, datatype=XSD.year)))

given_name_rdf()
revw_count_rdf()
yelping_since_rdf()
friends_rdf()
useful_votes_gvn_rdf()
funny_votes_gvn_rdf()
cool_votes_gvn_rdf()
fans_votes_rcvd_rdf()
cmplm_rcvd_rdf(cmplm_lst)
avg_stars_gvn_rdf()
years_w_elite_status_rdf()

#change this:
g.serialize(format="xml", destination="user_graph.xml")
