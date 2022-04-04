# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:18:27 2022

@author: MarcusA
"""

from nltk.corpus import wordnet

def synonym_antonym_extractor(phrase):
     synonyms = []
     antonyms = []

     for syn in wordnet.synsets(phrase):
          for l in syn.lemmas():
               synonyms.append(l.name())
               if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

     print(set(synonyms))
     print(set(antonyms))

#synonym_antonym_extractor(phrase="word")

synonyms = []

for syn in wordnet.synsets("Rehabilitation Center"):
    for i in syn.lemmas():
        synonyms.append(i.name())

print(set(synonyms))