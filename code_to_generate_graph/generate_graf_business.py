# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:20:34 2022

@author: ramme
"""

'''
packages json csv and pands are used for file manipulation

'''
import json
import csv 
import pandas as pd

'''
packages rdflib are used for creating tupples

'''

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD

from check_if_a_resource_exists_in_dbpedia import return_dbpedia_URI

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

def string_seperate_v2(string):
    '''

    Parameters
    ----------
    string : TYPE string
    
        takes a long string, that includes multiple strings seperated på comma.
        
    This function takes a string, 
    replaces '{' and  '}' with empty space,
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
    a_list = string.replace('{', '')
    a_list = a_list.replace('}', '')
    a_list = a_list.split(", ")
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

def add_line(string):
    '''
    

    Parameters
    ----------
    string : TYPE string
        a string.
        
    This function takes a string,
    replacing all empty spaces with line(_),
    then returns the transformed string

    Returns
    -------
    string : TYPE string
        transformed string.

    '''
    
    #replace empty space with _
    string = string.replace(" ", "_")
        
    return string




'''
The used prefixes.
schema is for schema.org
yelp_business is for yelp.com
db_resource is for dbpedia.org
own_URI is a fictional uri, that we created, which does not exist.
'''
schema = Namespace("https://schema.org/")
yelp_business = Namespace("https://www.yelp.com/biz/")
db_resource = Namespace("http://dbpedia.org/resource/")
yelp_ambience = Namespace("https://www.yelp.com/kg/biz/ambience/")
yelp_goodformeal = Namespace("https://www.yelp.com/kg/biz/goodformeal")
yelp_bestnights = Namespace("https://www.yelp.com/kg/biz/bestnights")



def graph_create_att():
    print('x')


if __name__ == "__main__":
    
    '''
    creating list to contain the file, that will be used to generate tripples
    '''
    csvfile = []
    cuisineList = []
    existdbList = []
    specialList = []
    
    '''
    Creating graph to contain the tripple, that will be used to generate tripples
    '''
    
    graph_file = open('business-yelp-test-kg.nt', 'a')

    '''
    Creating a dataframe for the state 
    open file line for line
    '''
    
    df = pd.read_csv('csvData.csv')
    
    '''
    Creating a list for existing cusines
    open file line for line
    '''
    
    with open('country_cusine_filtered_list.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            cuisineList.append(row[0])    
    '''
    Creating a list for existing cartegories 
    open file line for line
    '''
    with open('category_exist_in_db_List.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            existdbList.append(row[0])
    '''
    Creating a list for existing cartegories with special cartegories
    open file line for line
    '''
    with open('distinct_with_specialchar.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            specialList.append(row[0])
    '''
    open json file line for line
    for each line creates a business
    
    '''
    
    n = 0
    
    with open('yelp_academic_dataset_business.json', encoding="utf8") as f:
        for line in f:
            '''
            read line for line of the given json file 
            
            for each line read the line with json.loads
            cause we expect each line to be a json format.
            '''
            line = line.encode("ascii", "ignore") #removing unicode characters
            line = json.loads(line)
            g = Graph()
            
            '''
            for each element that exist as key in the line
            we check if any of the element are null values 
            we append all the element to a graph as a node.
            '''
            
            '''
            the name is appended as yelp_URI(subject) + legalName(predicate) + literal(object)
            '''
            if line['name'] != None:
                g.add((URIRef(yelp_business + line['business_id']), schema.legalName, Literal(line['name'], datatype=XSD.string)))
            '''
            the address is appended as yelp_URI(subject) + streetAddress(predicate) + literal(object)
            
            '''
            if line['address'] != None:
                g.add((URIRef(yelp_business + line['business_id']), schema.streetAddress, Literal(line['address'],datatype=XSD.string)))
            '''
            the state is appended as yelp_URI(subject) + streetAddress(predicate) + URI(object)
            where the URI is created by using the code_to_state function
            '''
            
            if line['state'] != None:
                g.add((URIRef(yelp_business + line['business_id']), schema.addressRegion, URIRef(db_resource + (code_to_state(line['state'])))))

            '''
            the address is appended as yelp_URI(subject) + streetAddress(predicate) + literal(object)
            something
            something
            something            
            '''
            
            '''
            if line['state'] !=None and line['city'] != None:
                if return_dbpedia_URI(line['city'] + ',_' + code_to_state(line['state'])) != False:
                    g.add((URIRef(yelp_business + line['business_id']), schema.starRating, URIRef(line['city'] + ',_' + code_to_state(line['state']))))
                elif return_dbpedia_URI(line['city']) != False:
                    g.add((URIRef(yelp_business + line['business_id']), schema.starRating, URIRef(line['city'], datatype=XSD.string)))
                else:
                    g.add((URIRef(yelp_business + line['business_id']), schema.starRating, Literal(line['city'], datatype=XSD.string)))
            '''
            '''
            the address is appended as yelp_URI(subject) + streetAddress(predicate) + literal(object)
            '''
            if line['postal_code'] !=None:
                g.add((URIRef(yelp_business + line['business_id']), schema.postalCode, Literal(line['postal_code'], datatype=XSD.string)))
            '''
            the address is appended as yelp_URI(subject) + streetAddress(predicate) + literal(object)
            '''
            if line['latitude'] != None and line['longitude'] !=None:
                g.add((URIRef(yelp_business + line['business_id']), schema.latitude, Literal(line['latitude'], datatype=XSD.float)))
                g.add((URIRef(yelp_business + line['business_id']), schema.longitude, Literal(line['longitude'], datatype=XSD.float)))
            '''
            the address is appended as yelp_URI(subject) + streetAddress(predicate) + literal(object)
            '''
            if line['stars'] != None:
                g.add((URIRef(yelp_business + line['business_id']), schema.starRating, Literal(line['stars'], datatype=XSD.string)))
            '''
            the address is appended as yelp_URI(subject) + streetAddress(predicate) + literal(object)
            '''
            if line['hours'] != None:
                for times in line['hours']:
                    g.add((URIRef(yelp_business + line['business_id']), schema.openingHours, Literal(times, datatype=XSD.string)))

            
            if line['attributes'] != None:
                if line['attributes'].__contains__('RestaurantsTakeOut'):
                    if (line['attributes']['RestaurantsTakeOut']) == 'True':
                        bn = BNode("business_att_RestaurantsTakeOut" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Take-out')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    if (line['attributes']['RestaurantsTakeOut']) == 'False':
                        bn = BNode("business_att_RestaurantsTakeOut" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'Take-out')))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Take-out')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('BusinessParking'):
                    s_v2_list = string_seperate_v2(line['attributes']['BusinessParking'])
                    for words in range(len(s_v2_list)):
                        if (s_v2_list[words]) == "'lot': True":
                            bn = BNode("business_att_BusinessParking_Lot" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Parking_lot')))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'lot': True":
                            bn = BNode("business_att_BusinessParking_Lot" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Parking_lot')))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'street': True":
                            bn = BNode("business_att_BusinessParking_Street" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Street')))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'street': True":
                            bn = BNode("business_att_BusinessParking_Street" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Street')))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'validated': True":
                            bn = BNode("business_att_BusinessParking_Validated" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Validated', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'validated': True":
                            bn = BNode("business_att_BusinessParking_Validated" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Validated', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'valet': True":
                            bn = BNode("business_att_BusinessParking_Valet" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Valet', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'valet': True":
                            bn = BNode("business_att_BusinessParking_Valet" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Valet', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'lot': False":
                            bn = BNode("business_att_BusinessParking_Lot" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Parking_lot')))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'lot': False":
                            bn = BNode("business_att_BusinessParking_Lot" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Parking_lot')))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'street': False":
                            bn = BNode("business_att_BusinessParking_Street" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Street')))
                            g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'street': False":
                            bn = BNode("business_att_BusinessParking_Street" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, URIRef(db_resource + 'Street')))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'validated': False":
                            bn = BNode("business_att_BusinessParking_Validated" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Validated', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'validated': False":
                            bn = BNode("business_att_BusinessParking_Validated" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Validated', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "'valet': False":
                            bn = BNode("business_att_BusinessParking_Valet" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Valet', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                        elif (s_v2_list[words]) == "u'valet': False":
                            bn = BNode("business_att_BusinessParking_Valet" + str(n))
                            g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                            g.add((bn, schema.additionalType, Literal('Valet', datatype=XSD.string)))
                            g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('Smoking'):
                    if (line['attributes']['Smoking']) == "'yes'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.smokingAllowed, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Smoking']) == "u'yes'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.smokingAllowed, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Smoking']) == "'no'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.smokingAllowed, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Smoking']) == "u'no'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.smokingAllowed, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('BusinessAcceptsCreditCards'):
                    if (line['attributes']['BusinessAcceptsCreditCards']) == 'True':
                        bn = BNode("business_att_CreditCards" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.paymentAccepted, bn))
                        g.add((bn, schema.additionalType, Literal('Credit_Card', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BusinessAcceptsCreditCards']) == 'False':
                        bn = BNode("business_att_CreditCards" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.paymentAccepted, bn))
                        g.add((bn, schema.additionalType, Literal('Credit_Card', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('BikeParking'):
                    if (line['attributes']['BikeParking']) == 'True':
                        bn = BNode("business_att_BikeParking" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Bicycle')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    if (line['attributes']['BikeParking']) == 'False':
                        bn = BNode("business_att_BikeParking" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.ParkingFacility, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Bicycle')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('RestaurantsPriceRange2'):
                    if (line['attributes']['RestaurantsPriceRange2']) == '1':
                        g.add((URIRef(yelp_business + line['business_id']), schema.priceRange, Literal('1')))
                    elif (line['attributes']['RestaurantsPriceRange2']) == '2':
                        g.add((URIRef(yelp_business + line['business_id']), schema.priceRange, Literal('2')))
                    elif (line['attributes']['RestaurantsPriceRange2']) == '3':
                        g.add((URIRef(yelp_business + line['business_id']), schema.priceRange, Literal('3')))
                    elif (line['attributes']['RestaurantsPriceRange2']) == '4':
                        g.add((URIRef(yelp_business + line['business_id']), schema.priceRange, Literal('4')))
                if line['attributes'].__contains__('CoatCheck'):
                    if (line['attributes']['CoatCheck']) == 'True':
                        bn = BNode("business_att_CoatCheck" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Wardrobe')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['CoatCheck']) == 'False':
                        bn = BNode("business_att_CoatCheck" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Wardrobe')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('RestaurantsDelivery'):
                    if (line['attributes']['RestaurantsDelivery']) == 'True':
                        bn = BNode("business_att_RestaurantsDelivery" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.DeliveryMethod, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Delivery_service')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['RestaurantsDelivery']) == 'False':
                        bn = BNode("business_att_RestaurantsDelivery" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.DeliveryMethod, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Delivery_service')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('Caters'):
                    if (line['attributes']['Caters']) == 'True':
                        bn = BNode("business_att_Caters" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.FoodEstablishment, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Catering')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Caters']) == 'False':
                        bn = BNode("business_att_Caters" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.FoodEstablishment, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Catering')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('WiFi'):
                    if (line['attributes']['WiFi']) == "'free'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'Wi-Fi')))
                    if (line['attributes']['WiFi']) == "u'free'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'Wi-Fi')))
                    if (line['attributes']['WiFi']) == "'paid'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'Wi-Fi')))
                    if (line['attributes']['WiFi']) == "u'paid'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'Wi-Fi')))
                if line['attributes'].__contains__('WheelchairAccessible'):
                    if (line['attributes']['WheelchairAccessible']) == 'True':
                        bn = BNode("business_att_WheelchairAccessible" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.accessibilityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Wheelchair')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['WheelchairAccessible']) == 'False':
                        bn = BNode("business_att_WheelchairAccessible" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.accessibilityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Wheelchair')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('HappyHour'):
                    if (line['attributes']['HappyHour']) == 'True':
                        bn = BNode("business_att_HappyHour" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Happy_Hour')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['HappyHour']) == 'False':
                        bn = BNode("business_att_HappyHour" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Happy_Hour')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('OutdoorSeating'):
                    if (line['attributes']['OutdoorSeating']) == 'True':
                        bn = BNode("business_att_HappyHour" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.containsPlace, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Outdoor_dining')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    if (line['attributes']['OutdoorSeating']) == 'False':
                        bn = BNode("business_att_HappyHour" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.containsPlace, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Outdoor_dining')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('HasTV'):
                    if (line['attributes']['HasTV']) == 'True':
                        bn = BNode("business_att_HasTV" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Television')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    if (line['attributes']['HasTV']) == 'False':
                        bn = BNode("business_att_HasTV" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Television')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('RestaurantsReservations'):
                    if (line['attributes']['RestaurantsReservations']) == 'True':
                        bn = BNode("business_att_RestaurantsReservations" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.acceptsReservations, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'RestaurantsReservations')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['RestaurantsReservations']) == 'False':
                        bn = BNode("business_att_RestaurantsReservations" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.acceptsReservations, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'RestaurantsReservations')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('DogsAllowed'):
                    if (line['attributes']['DogsAllowed']) == 'True':
                        g.add((URIRef(yelp_business + line['business_id']), schema.petsAllowed, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DogsAllowed']) == 'False':
                        g.add((URIRef(yelp_business + line['business_id']), schema.petsAllowed, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('Alcohol'):
                    if (line['attributes']['Alcohol']) == 'True':
                        bn = BNode("business_att_Alcohol" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.hasMenuItem, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Alcoholic_drink')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Alcohol']) == 'True':
                        bn = BNode("business_att_Alcohol" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.hasMenuItem, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Alcoholic_drink')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('GoodForKids'):
                    if (line['attributes']['GoodForKids']) == 'True':
                        bn = BNode("business_att_GoodForKids" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Family-friendly')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    if (line['attributes']['GoodForKids']) == 'False':
                        bn = BNode("business_att_GoodForKids" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Family-friendly')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('Ambience'):
                    if (line['attributes']['Ambience']) == "'romantic': True":
                        bn = BNode("business_att_Ambience_Romantic" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Romantic', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'romantic': True":
                        bn = BNode("business_att_Ambience_Romantic" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Romantic', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'intimate': True":
                        bn = BNode("business_att_Ambience_Intimate" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Intimate', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'intimate': True":
                        bn = BNode("business_att_Ambience_Intimate" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Intimate', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'touristy': True":
                        bn = BNode("business_att_Ambience_Touristy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Touristy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'touristy': True":
                        bn = BNode("business_att_Ambience_Touristy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Touristy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'hipster': True":
                        bn = BNode("business_att_Ambience_Hipster" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Hipster', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'hipster': True":
                        bn = BNode("business_att_Ambience_Hipster" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Hipster', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'divey': True":
                        bn = BNode("business_att_Ambience_Hipster_Divey" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Divey', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'divey': True":
                        bn = BNode("business_att_Ambience_Hipster_Divey" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Divey', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'trendy': True":
                        bn = BNode("business_att_Ambience_Hipster_Trendy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Trendy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'trendy': True":
                        bn = BNode("business_att_Ambience_Hipster_Trendy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Trendy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'upscale': True":
                        bn = BNode("business_att_Ambience_Hipster_Upscale" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Upscale', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'upscale': True":
                        bn = BNode("business_att_Ambience_Hipster_Upscale" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Upscale', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'classy': True":
                        bn = BNode("business_att_Ambience_Hipster_Classy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Classy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'classy': True":
                        bn = BNode("business_att_Ambience_Hipster_Classy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Classy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'casual': True":
                        bn = BNode("business_att_Ambience_Hipster_Casual" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Casual', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'casual': True":
                        bn = BNode("business_att_Ambience_Hipster_Casual" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Casual', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'romantic': False":
                        bn = BNode("business_att_Ambience_Romantic" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Romantic', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'romantic': False":
                        bn = BNode("business_att_Ambience_Romantic" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Romantic', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'intimate': False":
                        bn = BNode("business_att_Ambience_Intimate" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Intimate', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'intimate': False":
                        bn = BNode("business_att_Ambience_Intimate" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Intimate', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'touristy': False":
                        bn = BNode("business_att_Ambience_Touristy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Touristy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'touristy': False":
                        bn = BNode("business_att_Ambience_Touristy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Touristy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'hipster': False":
                        bn = BNode("business_att_Ambience_Hipster" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Hipster', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'hipster': False":
                        bn = BNode("business_att_Ambience_Hipster" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Hipster', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'divey': False":
                        bn = BNode("business_att_Ambience_Hipster_Divey" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Divey', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'divey': False":
                        bn = BNode("business_att_Ambience_Hipster_Divey" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Divey', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'trendy': False":
                        bn = BNode("business_att_Ambience_Hipster_Trendy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Trendy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'trendy': False":
                        bn = BNode("business_att_Ambience_Hipster_Trendy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Trendy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'upscale': False":
                        bn = BNode("business_att_Ambience_Hipster_Upscale" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Upscale', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'upscale': False":
                        bn = BNode("business_att_Ambience_Hipster_Upscale" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Upscale', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'classy': False":
                        bn = BNode("business_att_Ambience_Hipster_Classy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Classy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'classy': False":
                        bn = BNode("business_att_Ambience_Hipster_Classy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Classy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "'casual': False":
                        bn = BNode("business_att_Ambience_Hipster_Casual" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Casual', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['Ambience']) == "u'casual': False":
                        bn = BNode("business_att_Ambience_Hipster_Casual" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_ambience, bn))
                        g.add((bn, schema.additionalType, Literal('Casual', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('RestaurantsTableService'):
                    if (line['attributes']['RestaurantsTableService']) == 'True':
                        bn = BNode("business_att_RestaurantsTableService" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Waiting_staff')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    if (line['attributes']['RestaurantsTableService']) == 'False':
                        bn = BNode("business_att_RestaurantsTableService" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Waiting_staff')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('DriveThru'):
                    if (line['attributes']['DriveThru']) == 'True':
                        bn = BNode("business_att_DriveThru" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Drive-through')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DriveThru']) == 'False':
                        bn = BNode("business_att_DriveThru" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Drive-through')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('NoiseLevel'):
                    if (line['attributes']['NoiseLevel']) == "'average'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Average', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "u'average'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Average', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "'quiet'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Quiet', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "u'quiet'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Quiet', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "'loud'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Loud', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "u'loud'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Loud', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "u'very_loud'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Very_loud', datatype=XSD.string)))
                    elif (line['attributes']['NoiseLevel']) == "u'very_loud'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.Level, Literal('Very_loud', datatype=XSD.string)))
                if line['attributes'].__contains__('GoodForMeal'):
                    if (line['attributes']['GoodForMeal']) == "'dessert': True":
                        bn = BNode("business_att_GoodForMeal_Dessert" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'dessert': True":
                        bn = BNode("business_att_GoodForMeal_Dessert" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'brunch': True":
                        bn = BNode("business_att_GoodForMeal_Brunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, Literal('Brunch', datatype=XSD.string)))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'brunch': True":
                        bn = BNode("business_att_GoodForMeal_Brunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, Literal('Brunch', datatype=XSD.string)))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'breakfast': True":
                        bn = BNode("business_att_GoodForMeal_Breakfast" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Breakfast', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'breakfast': True":
                        bn = BNode("business_att_GoodForMeal_Breakfast" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Breakfast', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'lunch': True":
                        bn = BNode("business_att_GoodForMeal_Lunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Lunch', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'lunch': True":
                        bn = BNode("business_att_GoodForMeal_Lunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Lunch', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'dinner': True":
                        bn = BNode("business_att_GoodForMeal_Dinner" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dinner', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'dinner': True":
                        bn = BNode("business_att_GoodForMeal_Dinner" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dinner', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'latenight': True":
                        bn = BNode("business_att_GoodForMeal_Latenight" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Latenight', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'latenight': True":
                        bn = BNode("business_att_GoodForMeal_Latenight" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Latenight', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    
                    if (line['attributes']['GoodForMeal']) == "'dessert': False":
                        bn = BNode("business_att_GoodForMeal_Dessert" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'dessert': False":
                        bn = BNode("business_att_GoodForMeal_Dessert" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'brunch': False":
                        bn = BNode("business_att_GoodForMeal_Brunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, Literal('Brunch', datatype=XSD.string)))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'brunch': False":
                        bn = BNode("business_att_GoodForMeal_Brunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, Literal('Brunch', datatype=XSD.string)))
                        g.add((bn, schema.additionalType, Literal('Dessert', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'breakfast': False":
                        bn = BNode("business_att_GoodForMeal_Breakfast" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Breakfast', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'breakfast': False":
                        bn = BNode("business_att_GoodForMeal_Breakfast" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Breakfast', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'lunch': False":
                        bn = BNode("business_att_GoodForMeal_Lunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Lunch', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'lunch': False":
                        bn = BNode("business_att_GoodForMeal_Lunch" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Lunch', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'dinner': False":
                        bn = BNode("business_att_GoodForMeal_Dinner" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dinner', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'dinner': False":
                        bn = BNode("business_att_GoodForMeal_Dinner" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Dinner', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "'latenight': False":
                        bn = BNode("business_att_GoodForMeal_Latenight" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Latenight', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForMeal']) == "u'latenight': False":
                        bn = BNode("business_att_GoodForMeal_Latenight" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_goodformeal, bn))
                        g.add((bn, schema.additionalType, Literal('Latenight', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean))) 
                if line['attributes'].__contains__('BusinessAcceptsBitcoin'):
                    if (line['attributes']['BusinessAcceptsBitcoin']) == 'True':
                        bn = BNode("business_att_Cryptocurrency" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.paymentAccepted, bn))
                        g.add((bn, schema.additionalType, Literal('Cryptocurrency', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BusinessAcceptsBitcoin']) == 'False':
                        bn = BNode("business_att_Cryptocurrency" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.paymentAccepted, bn))
                        g.add((bn, schema.additionalType, Literal('Cryptocurrency', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('Music'):
                    if (line['attributes']['Music']) == 'True':
                        bn = BNode("business_att_Music" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Music')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['Music']) == 'False':
                        bn = BNode("business_att_Music" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Music')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('GoodForDancing'):
                    if (line['attributes']['GoodForDancing']) == 'True':
                        bn = BNode("business_att_Dance" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Dance')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['GoodForDancing']) == 'False':
                        bn = BNode("business_att_Dance" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'Dance')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('AcceptsInsurance'):
                    if (line['attributes']['AcceptsInsurance']) == 'True':
                        bn = BNode("business_att_Insurance" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.paymentAccepted, bn))
                        g.add((bn, schema.additionalType, Literal('Insurance', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['AcceptsInsurance']) == 'False':
                        bn = BNode("business_att_Insurance" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.paymentAccepted, bn))
                        g.add((bn, schema.additionalType, Literal('Insurance', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('BestNights'):
                    if (line['attributes']['BestNights']) == "'monday': True":
                        bn = BNode("business_att_BestNights_Monday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Monday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'monday': True":
                        bn = BNode("business_att_BestNights_Monday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Monday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'tuesday': True":
                        bn = BNode("business_att_BestNights_Tuesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Tuesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'tuesday': True":
                        bn = BNode("business_att_BestNights_Tuesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Tuesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'wednesday': True":
                        bn = BNode("business_att_BestNights_Wednesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Wednesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'wednesday': True":
                        bn = BNode("business_att_BestNights_Wednesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Wednesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'thursday': True":
                        bn = BNode("business_att_BestNights_Thursday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Thursday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'thursday': True":
                        bn = BNode("business_att_BestNights_Thursday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Thursday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'friday': True":
                        bn = BNode("business_att_BestNights_Friday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Friday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'friday': True":
                        bn = BNode("business_att_BestNights_Friday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Friday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'saturday': True":
                        bn = BNode("business_att_BestNights_Saturday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Saturday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'saturday': True":
                        bn = BNode("business_att_BestNights_Saturday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Saturday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'sunday': True":
                        bn = BNode("business_att_BestNights_Sunday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Sunday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'sunday': True":
                        bn = BNode("business_att_BestNights_Sunday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Sunday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        
                    elif (line['attributes']['BestNights']) == "'monday': False":
                        bn = BNode("business_att_BestNights_Monday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Monday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'monday': False":
                        bn = BNode("business_att_BestNights_Monday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Monday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'tuesday': False":
                        bn = BNode("business_att_BestNights_Tuesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Tuesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'tuesday': False":
                        bn = BNode("business_att_BestNights_Tuesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Tuesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'wednesday': False":
                        bn = BNode("business_att_BestNights_Wednesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Wednesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'wednesday': False":
                        bn = BNode("business_att_BestNights_Wednesday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Wednesday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'thursday': False":
                        bn = BNode("business_att_BestNights_Thursday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Thursday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'thursday': False":
                        bn = BNode("business_att_BestNights_Thursday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Thursday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'friday': False":
                        bn = BNode("business_att_BestNights_Friday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Friday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'friday': False":
                        bn = BNode("business_att_BestNights_Friday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Friday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'saturday': False":
                        bn = BNode("business_att_BestNights_Saturday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Saturday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'saturday': False":
                        bn = BNode("business_att_BestNights_Saturday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Saturday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "'sunday': False":
                        bn = BNode("business_att_BestNights_Sunday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Sunday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                    elif (line['attributes']['BestNights']) == "u'sunday': False":
                        bn = BNode("business_att_BestNights_Sunday" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), yelp_bestnights, bn))
                        g.add((bn, schema.additionalType, Literal('Sunday', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('BYOB'):
                    if (line['attributes']['BYOB']) == 'True':
                        bn = BNode("business_att_BYOB" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'BYOB')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['BYOB']) == 'False':
                        bn = BNode("business_att_BYOB" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'BYOB')))
                        g.add((bn, schema.value, Literal('False', datatype=XSD.boolean)))
                if line['attributes'].__contains__('corkage'):
                    if (line['attributes']['corkage']) == 'True':
                        bn = BNode("business_att_Corkage" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, bn))
                        g.add((bn, schema.additionalType, URIRef(db_resource + 'BYOB')))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                if line['attributes'].__contains__('BYOBCorkage'):
                    if (line['attributes']['BYOBCorkage']) == "'yes_free'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'BYOB')))
                    if (line['attributes']['BYOBCorkage']) == "'yes_corkage'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'BYOB')))
                    if (line['attributes']['BYOBCorkage']) == "u'yes_free'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'BYOB')))
                    if (line['attributes']['BYOBCorkage']) == "u'yes_corkage'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.amenityFeature, URIRef(db_resource + 'BYOB')))
                if line['attributes'].__contains__('AgesAllowed'):
                    if (line['attributes']['AgesAllowed']) == "u'18plus'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.suggestedAge, Literal('18+')))
                    if (line['attributes']['AgesAllowed']) == "u'21plus'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.suggestedAge, Literal('21+')))
                    if (line['attributes']['AgesAllowed']) == "u'allages'":
                        g.add((URIRef(yelp_business + line['business_id']), schema.suggestedAge, Literal('All_Ages')))
                if line['attributes'].__contains__('DietaryRestrictions'):
                    if (line['attributes']['DietaryRestrictions']) == "'dairy-free': True":
                        bn = BNode("business_att_DietaryRestrictions_Dairy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Dairy-free', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DietaryRestrictions']) == "'gluten-free': True":
                        bn = BNode("business_att_DietaryRestrictions_Gluten" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Gluten-free', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DietaryRestrictions']) == "'vegan': True":
                        bn = BNode("business_att_DietaryRestrictions_Vegan" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Vegan', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DietaryRestrictions']) == "'kosher': True":
                        bn = BNode("business_att_DietaryRestrictions_Kosher" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Kosher', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DietaryRestrictions']) == "'halal': True":
                        bn = BNode("business_att_DietaryRestrictions_Halal" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Halal', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DietaryRestrictions']) == "'soy-free': True":
                        bn = BNode("business_att_DietaryRestrictions_Soy" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Soy', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                    elif (line['attributes']['DietaryRestrictions']) == "'vegetarian': True":
                        bn = BNode("business_att_DietaryRestrictions_Vegetarian" + str(n))
                        g.add((URIRef(yelp_business + line['business_id']), schema.RestrictedDiet, bn))
                        g.add((bn, schema.additionalType, Literal('Vegetarian', datatype=XSD.string)))
                        g.add((bn, schema.value, Literal('True', datatype=XSD.boolean)))
                        
            
            graph_file.write(g.serialize(format="nt"))
            print(n)
            
            n = n + 1
        
graph_file.close()