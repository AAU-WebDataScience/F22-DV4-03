# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:11:48 2022

@author: ramme
"""
from urllib.error import HTTPError
from SPARQLWrapper import SPARQLWrapper, JSON 
import traceback
import logging


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
    try:
      sparql.setReturnFormat(JSON)
    except Exception as e:
        return False
    
    try:
      res = sparql.query().convert()
    except Exception as e:
        return False
    
    
    
    return res['boolean']