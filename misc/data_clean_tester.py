# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 19:57:37 2022

@author: MarcusA
"""

import csv 
import pandas as pd

'''
#create list for cuisine
list_cusine = sql_country_cusine
for element in range(len(data_business)):
    distinct_list = string_seperate(element)
    for category in distinct_list
        check_cate(category)
        
'''


from check_if_a_resource_exists_in_dbpedia import check_exist_dbpedia

def check_catagory_with_dbpedia():
    #check if category exist in 
    newnewList = []
    goodList = []
    badList = []
    
    with open('category_list_goodList_v2.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            newnewList.append(row[0])
    #check if categpry exist in dbpedia
    
    for n in range(len(newnewList)):
        #return true or false
        if check_exist_dbpedia(newnewList[n]) == True:
            #add to goodList if true
            goodList.append(newnewList[n])
        else:
            #add to badList if else
            badList. append(newnewList[n])
           
    df = pd.DataFrame(goodList) 
        
    #saving the dataframe 
    df.to_csv('category_list_goodList.csv', index = False)
    
    df2 = pd.DataFrame(badList) 
        
    #saving the dataframe 
    df2.to_csv('category_list_badList.csv', index = False)


def create_distinct_list(data_business):
    #create a create_distinct_list
    n = 0
    distinct_list = []
    for element in range(len(data_business)):
        if data_business[n]['categories'] != None:
            string = data_business[n]['categories']
            a_list = string.split(", ")
            for element in a_list:
                if element not in distinct_list:
                    distinct_list.append(element)
        n = n +1
    return distinct_list


'''
def no_specialchar_or_cusine():
    #create list that contains no specialchar or cusine
    no_char = []
    cuisine = []
    
    with open('distinct_no_specialchar.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            no_char.append(row[0])
            
    with open('country_cusine_list.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            cusine.append(row[0])
            
    distinct_no_specialchar_or_cuisine = [x for x in no_char if x not in cusine]
    
    df3 = pd.DataFrame(distinct_no_specialchar_or_cuisine) 
        
    #saving the dataframe 
    df3.to_csv('distinct_no_specialchar_or_cuisine.csv', index = False)

'''



def add_line_to_empty_list():
    
    newList = []
        
    with open('distinct_no_specialchar.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            newList.append(row[0])
    n = 0   
    for i in newList:  
        newList[n] = newList[n].lower()
        n = n +1
        
    n = 0
    for i in newList:  
        newList[n] = newList[n].capitalize()
        n = n +1
        
    n = 0
    for i in newList:   
        newList[n] = newList[n].replace(" ", "_")
        n = n +1
            
    df = pd.DataFrame(newList)
    
    df.to_csv('category_list_goodList_v2.csv', index = False)

check_catagory_with_dbpedia()