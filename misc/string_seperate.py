# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:15:50 2022

@author: MarcusA
"""

def string_seperate(string):
    n = 0
    cate_list = []
    a_list = string.split(", ")
    for element in a_list:
        cate_list.append(element)
    n = n +1
    return cate_list
