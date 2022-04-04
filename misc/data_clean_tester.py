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

def sort_exist():
    sortedList_x1 = []
    
    existdbList = []
    
    notexistdbList = []
    
    with open('distinct_no_specialchar.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            sortedList_x1.append(row[0])
    '''      
    for element in sortedList_x1:
        if check_exist_dbpedia(element) == True:
            existdbList.append(element)
    '''
    df_exist = pd.DataFrame(existdbList) 
    
    
    for element in sortedList_x1:
        if check_exist_dbpedia(element) == False:
            notexistdbList.append(element)
    
    df_not_exist = pd.DataFrame(notexistdbList)


    with open('distinct_with_specialchar.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            sortedList_x1.append(row[0])
            
def add_line_to_emptylist():
    newList = []
    newList2 = []
            
    with open('category_notexist_in_db_List.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            newList.append(row[0])
            newList2.append(row[0])
            
    n = 0   
    for i in newList:  
            newList[n] = newList[n].lower()
            n = n + 1
            
    n = 0
    for i in newList:   
        newList[n] = newList[n].replace(" ", "_")
        n = n + 1
            
    n = 0
    for i in newList:  
        newList[n] = newList[n].capitalize()
        n = n + 1
    
    
    existList2 = pd.DataFrame(columns=['0', '1'])
    notexistList2 = pd.DataFrame(columns=['0'])
    
    n = 0
    for element in newList:
        if check_exist_dbpedia(element) == True:
            existList2 = existList2.append({'0': newList2[n], '1':element}, ignore_index=True)
        elif check_exist_dbpedia(element) == False:
            notexistList2 = notexistList2.append({'0':newList2[n]}, ignore_index=True)
        n = n + 1
        
        
    existList2.to_csv('category_exist_in_db_List_v2.csv', index = False)
    notexistList2.to_csv('category_notexist_in_db_List_v2.csv', index = False)


def string_seperate_special(string):
    n = 0
    split_list = []
    a_list = string.split(" & ")
    for element in a_list:
        split_list.append(element)
    n = n + 1
    return split_list

def change_to_line(string):
#takes a string, change to lower case,
#then replace empty space and change to line
#capitalice first letter
    string = string.lower()
    string = string.replace(" ", "_")
    string = string.capitalize()
    return string

def change_to_singular():
    notexistList2v2 = pd.read_csv('category_notexist_in_db_List_v2.csv', header=None)
    
    from pattern.text.en import singularize
    
    singular_list = []
    
    n = 0
    for index, row in notexistList2v2.iterrows():
        singular_list.append(singularize(row[0]))
        n = n + 1
    
    existListv3 = df = pd.DataFrame(columns=['0', '1'])
    notexistListv3 = df = pd.DataFrame(columns=['0', '1'])
    
    
    n = 0
    for element in singular_list:
        if check_exist_dbpedia(element) == True:
            existListv3 = existListv3.append({'0': notexistList2v2[0][n],'1': element}, ignore_index=True)
        elif check_exist_dbpedia(element) == False:
            notexistListv3 = notexistListv3.append({'0':notexistList2v2[0][n], '1': element}, ignore_index=True)
        n = n + 1
    
    existListv3.to_csv('category_exist_in_db_List_v3.csv', index = False)
    notexistListv3.to_csv('category_notexist_in_db_List_v3.csv', index = False)


def split_special():
    notexistList_special_v1 = pd.read_csv('distinct_with_specialchar2.csv', header=None)
    
    special_character_1 = "/"
    # Example: $tackoverflow
    
    sorted_special_list = pd.DataFrame(columns=['0', '1', '2'])
    
    n = 0
    for index, row in notexistList_special_v1.iterrows():
        string = row[0]
        if any(c in special_character_1 for c in string):
            list_1 = (row[0]).split("/")
        else:
            list_1 = (row[0]).split(" & ")
        sorted_special_list = sorted_special_list.append({'0':row[0], '1': list_1[0],'2': list_1[1]}, ignore_index=True)
        n = n + 1
        
    sorted_special_list.to_csv('category_special_sorted_List_v3.csv', index = False)

def special_singular():
    singel_special = pd.read_csv('category_special_sorted_List_v3.csv', header=None)
    
    from pattern.text.en import singularize
    
    n = 0
    for index, row in singel_special.iterrows():
        
        sing_word = singularize(row[1])
        singel_special.iat[n,1] = sing_word
        sing_word = singularize(row[2])
        singel_special.iat[n,2] = sing_word
        
        n = n +1
    
    singel_special.to_csv('category_special_singeled.csv', index = False)

def special_add_lines():

    addline_special = pd.read_csv('category_special_singeled.csv', header=None)
    
    n = 0
    for index, row in addline_special.iterrows():
        
        sing_word = change_to_line(row[1])
        addline_special.iat[n,1] = sing_word
        sing_word = change_to_line(row[2])
        addline_special.iat[n,2] = sing_word
        
        n = n +1
    
    addline_special.to_csv('category_special_withlines.csv', index = False)


def special_exist_in_db():
    exist_in_db = pd.read_csv('category_special_withlines.csv', header=None)
    
    existList_spv1 = pd.DataFrame(columns=['0','1','2'])
    notexistList_spv1 = pd.DataFrame(columns=['0','1','2'])
    
    
    n = 0
    for index, row in exist_in_db.iterrows():
        if check_exist_dbpedia(row[1]) == True and check_exist_dbpedia(row[2]) == True:
            existList_spv1 = existList_spv1.append({'0':row[0], '1': row[1],'2': row[2]}, ignore_index=True)
        elif check_exist_dbpedia(row[1]) == True and check_exist_dbpedia(row[2]) == False:
            existList_spv1 = existList_spv1.append({'0':row[0], '1': row[1]}, ignore_index=True)
            notexistList_spv1 = notexistList_spv1.append({'0':row[0],'2': row[2]}, ignore_index=True)
        elif check_exist_dbpedia(row[1]) == False and check_exist_dbpedia(row[2]) == True:
            existList_spv1 = existList_spv1.append({'0':row[0], '2': row[2]}, ignore_index=True)
            notexistList_spv1 = notexistList_spv1.append({'0':row[0],'1': row[1]}, ignore_index=True)
        else:
            notexistList_spv1 = notexistList_spv1.append({'0':row[0], '1': row[1],'2': row[2]}, ignore_index=True)
        n = n + 1
    
    existList_spv1.to_csv('category_special_exist_v1.csv', index = False)
    notexistList_spv1.to_csv('category_special_notexist_v1.csv', index = False)
