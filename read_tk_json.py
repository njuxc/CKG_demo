# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:25:15 2023

@author: 11834
"""

import json
import Levenshtein
import difflib

def get_score(t1,t2):
    print(t1,t2)
    temp = 0
    for i in t2:
        if i in t1:
            temp = temp + 1
    fenmu = len(t1) + len(t2) - temp  # 并集
    jaccard_coefficient = float(temp / fenmu)
    s1= jaccard_coefficient
    s2=Levenshtein.ratio(t1, t2)
    s3=difflib.SequenceMatcher(None, t1, t2).quick_ratio()
    return s1,s2,s3

with open('tmp.json','r') as f:
    tk_dict=json.load(f)

#print(type(tk_dict))
#print(tk_dict)

possible_tokens=set()

for sentence in  tk_dict['sentences']:
    tokens=sentence['tokens']
    for token in tokens:
        if token['ner']=='CodeToken':
            possible_tokens.add(token['word'])
            
#print(possible_tokens)

code_tokens=['self._sync_metadata(result)']

for ctoken in code_tokens:
    for ptoken in possible_tokens:
        score=get_score(ctoken,ptoken)
        print(score)