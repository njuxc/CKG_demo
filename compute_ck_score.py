# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:33:31 2023

@author: 11834
"""

import os,sys
import json
import Levenshtein
import difflib
from codeChange import get_code_change

def get_c_changes(proj,cid):
    logdir='commit_files/'+proj+'/'+cid+'/'
    try:
        files=os.listdir(logdir)
    except Exception:
        print('File is missing!')
        return []
    ret=[]
    print(logdir)
    print(files)
    for file in files:
        if file.startswith('changelog_'):
            logf=logdir+file
            fname=file.split('changelog_')[1]
            oldfile=logdir+fname
            newf=''
            changes=get_code_change(logf,oldfile,newf)
            ret.extend(changes)
    return ret

def get_tinfo(cpath):
    jsons=os.listdir(cpath)
    #print(jsons)
    #sys.exit()
    possible_tokens=set()
    for js in jsons:
        with open(cpath+'/'+js) as f:
            tk_dict=json.load(f)
            #print(tk_dict)
        for sentence in  tk_dict['sentences']:
            tokens=sentence['tokens']
            for token in tokens:
                if token['ner']=='CodeToken':
                    possible_tokens.add(token['word'])
    #print(possible_tokens)
    #sys.exit()
    return possible_tokens

def count_score(t1,t2):
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

def get_score(code_tokens,possible_tokens):
    
    sret=[]
    for ctoken in code_tokens:
        for ptoken in possible_tokens:
            score=count_score(ctoken,ptoken)
            #print(score)
            sret.append(score)
    return sret

#projs=['django', 'scikit-learn','pandas','ansible','airflow','keras']
projs=['airflow']

for proj in projs:
    dir_name='jsons/'+proj+'/'
    files=os.listdir(dir_name)
    #print(files)
    for cid in files:
        #print(proj,cid)
        cchanges=get_c_changes(proj,cid)
        print(cchanges)
        if len(cchanges)==0:
            continue
        #sys.exit()
        token_ners=get_tinfo(dir_name+cid)
        print(token_ners)
        score=get_score(cchanges,token_ners)
        print(score)
        #sys.exit()