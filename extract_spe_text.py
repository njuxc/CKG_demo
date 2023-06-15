# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:39:30 2022

@author: 11834
"""

from tqdm import tqdm
import binascii
from git import Repo
import os,sys
import difflib
import numpy as np

projs=['django', 'scikit-learn','pandas','ansible','airflow','keras']
#projs=['airflow']
label='redundantCall/'

for proj in projs:

    with open('csvs/'+label+proj+'.csv') as f:
        lines=f.readlines()
    
    tcommits=[]
    
    for line in lines:
        line = line.strip()
        tcommits.append(line)
    
    tcommits=list(set(tcommits))
    #print(tcommits)
    
    repo = Repo(proj)
    commits = list(repo.iter_commits())
    
    for commit in tqdm(commits):
        cid=binascii.b2a_hex(commit.binsha).decode("utf-8")
        if not cid in tcommits:
            continue
            
        mess=commit.message
    
        with open('commit_texts/'+label+proj+'/'+cid+'.txt','w+') as fi:
            fi.write(mess)
