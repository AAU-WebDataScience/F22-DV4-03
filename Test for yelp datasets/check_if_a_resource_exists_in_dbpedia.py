# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:11:48 2022

@author: ramme
"""

from SPARQLWrapper import SPARQLWrapper, JSON 

def check_exist_dbpedia(category):

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    
    sparql.setQuery("""
        PREFIX dbr: <http://dbpedia.org/resource/>
    ASK {
        VALUES (?r) { (dbr:"""+str(category)+""") }
            { ?r ?p ?o }
            UNION
            { ?s ?r ?o }
            UNION
            { ?s ?p ?r }
        } 
                    """)
    
    sparql.setReturnFormat(JSON)
    
    res = sparql.query().convert()
    
    
    return res['boolean']


#print(check_exist_dbpedia('Restaurant'))