# -*- coding: utf-8 -*-
"""
Created on Mon May 16 08:09:33 2022

@author: MarcusA
"""

import json
import csv 
import pandas as pd

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD

data_business = []
data_business_cuisine = []
csvfile = []
cuisineList = []
existdbList = []
specialList = []

from check_if_a_resource_exists_in_dbpedia import return_dbpedia_URI
from check_if_a_resource_exists_in_dbpedia import check_exist_dbpedia
from pattern.text.en import singularize

        
df = pd.read_csv('csvData.csv')

schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
db_resource = Namespace("http://dbpedia.org/resource/")

def change_format_to_db(catagory):
    '''
    

    Parameters
    ----------
    catagory : TYPE string
        takes a string in catagory from yelp.
        
    This function takes a string in catagory from yelp,
    changes string to lower case,
    capitalize the first letter in string,
    replace all empty spaces with line(_),
    then returns the transformed string

    Returns
    -------
    newcatagory : TYPE string
        retuens transformed string.

    '''
    #changes the whole string to lower case,
    newcatagory = catagory.lower()
    
    #capitalize first letter 
    newcatagory = catagory.capitalize()
    
    #replace empty space with _
    newcatagory = catagory.replace(" ", "_")
    
    return newcatagory

def string_seperate(string):
    '''

    Parameters
    ----------
    string : TYPE string
    
        takes a long string, that includes multiple strings seperated på comma.
        
    This function takes a string, 
    seperate the string for each comma(,),
    and then append each element to a list,
    then returns the list.

    Returns
    -------
    cate_list : TYPE List
        list of string.

    '''
    n = 0
    cate_list = []
    a_list = string.split(", ")
    for element in a_list:
        cate_list.append(element)
    n = n +1
    return cate_list

def code_to_state(code):
    '''
    

    Parameters
    ----------
    code : TYPE string
        takes a string, that indicating a state code.
        
    This function takes a string,
    looping for every row in the df dataframe,
    compare it to all the values in the df dataframe,
    if a corresponding string exist in the Code column,
    then returns the string in the state column.
    

    Returns
    -------
    TYPE string
        string of a state.

    '''
    n = 0
    for index, row in df.iterrows():
        if str(code) == str(df.loc[n,'Code']):
            return str(df.loc[n,'State'])
        #str(df.loc[n,])
        n = n + 1
      
n = 0




def check_special_cate(string):
    
    if any(char not in special_characters for char in string):
        if ('&' in string) == True:
            string = string.replace('&', ' ')
            return  check_special_cate(string)
        elif ('/' in string) == True:
            string = string.replace('/', ' ')
            return  check_special_cate(string)
        elif ('(' in string) == True and (')' in string) == True:
            string = string.replace('(', ' ')
            string = string.replace(')', ' ')
            return  check_special_cate(string)
        elif ('   ' in string) == True:
            string = string.replace('   ', ' ')
            return  check_special_cate(string)
        elif ('  ' in string) == True:
            string = string.replace('  ', ' ')
            return  check_special_cate(string)
    return string


def add_singel_to_dbpedia(business_id,string):
    string = singularize(string)
    g.add((URIRef(yelp_business + business_id), schema.category, URIRef(db_resource + string)))
    
def remove_apo(string):
    return string.replace("'", "")

def check_exist_dbpedia_clone(business_id, string):
    
    db_list = ['Bubble Tea', 'Fast Food','Hot Dogs','Asian Fusion','Soul Food','Acai Bowls','Food Court','Dim Sum','Hot Pot','Tui Na']
    for element in db_list:
        if str(element) == string:
            g.add((URIRef(yelp_business + business_id), schema.category, URIRef(db_resource + change_format_to_db(element))))
            return True
    
def add_combined_to_dbpedia(business_id,string):
    
    if (' ' in string) == True and check_exist_dbpedia_clone(business_id,string) == True:
        return True
    elif (' ' in string) == True:
        string = string.split()
        for word in string:
            word = singularize(word)
            g.add((URIRef(yelp_business + business_id), schema.category, URIRef(db_resource + word)))
    elif (' ' in string) != True:
        string = singularize(string)
        g.add((URIRef(yelp_business + business_id), schema.category, URIRef(db_resource + word)))
    
            
    
    '''
    if check_exist_dbpedia(change_format_to_db(string)) == True:
        g.add((URIRef(yelp_business + line['business_id']), schema.category, URIRef(db_resource + change_format_to_db(string))))
    else:
    '''
    
graph_file = open('yelp-kg-business_ex_cate.nt', 'a')

with open('yelp_academic_dataset_business.json', encoding="utf8") as f:
    for line in f:
        line = line.encode("ascii", "ignore") #removing unicode characters
        line = json.loads(line)
        g = Graph()
        special_characters = "^&()/"        
        if line['categories'] != None:
            #split the string in categories to a list, create list as catagory_list
            catagory_list = string_seperate(line['categories'])
            #for every item in catagory_list, compare it with the dbpedia
            for item in catagory_list:
                item = remove_apo(item)
                if any(char in special_characters for char in item):
                    item = check_special_cate(item)
                    if (' ' in item) == True:
                        add_combined_to_dbpedia(line['business_id'],item)
                    else:
                        words = remove_apo(item)
                        add_singel_to_dbpedia(line['business_id'],item)
                elif (' ' in item) == True:
                    add_combined_to_dbpedia(line['business_id'],item)
                else:
                    add_singel_to_dbpedia(line['business_id'],item)
        graph_file.write(g.serialize(format="nt"))
        print(n)
            
        n = n + 1
graph_file.close()



'''
if line['state'] !=None and line['city'] != None:
    city = return_dbpedia_URI(change_format_to_db(line['city']) + ',_' + code_to_state(line['state']))
    print(line['city'] + ',_' + code_to_state(line['state']))
    if city != False:
        g.add((URIRef(yelp_business + line['business_id']), schema.City, URIRef(city)))
        print(city)
    elif return_dbpedia_URI(change_format_to_db(line['city'])) != False:
        g.add((URIRef(yelp_business + line['business_id']), schema.City, URIRef(db_resource + change_format_to_db(line['city']))))
        print(line['city'])
    else:
        g.add((URIRef(yelp_business + line['business_id']), schema.City, Literal(line['city'], datatype=XSD.string)))

g.add((URIRef(yelp_business + line['business_id']), schema.City, Literal(line['city'], datatype=XSD.string)))
'''