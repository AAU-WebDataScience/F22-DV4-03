# -*- coding: utf-8 -*-
"""
Created on Tue May 24 09:44:45 2022

@author: storm
"""
import csv

file = open("amount_of_user_reviews.csv")
reader = csv.reader(file)
lines= len(list(reader))
print(lines)