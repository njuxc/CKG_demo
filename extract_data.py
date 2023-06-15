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

with open('airflow.csv') as f:
    lines=f.readlines()
    
tcommits=[]

for line in lines:
    line = line.strip()
    tcommits.append(line)

tcommits=list(set(tcommits))
#print(tcommits)

repo = Repo("airflow/")
commits = list(repo.iter_commits())

total_features=''

for commit in tqdm(commits):
    cid=binascii.b2a_hex(commit.binsha).decode("utf-8")
    if not cid in tcommits:
        continue
    #target_dir='data/airflow1/'+cid
    #if not os.path.exists(target_dir):
        #os.makedirs(target_dir)
    print(cid)
    files=commit.stats.files.keys()
    for f in files:
        if f.endswith('.py'):
            #print('commit files:'+str(commit.stats.files)+'\n')
            #sys.exit()
            newf=f.replace('/','#')
            print(f,newf)
            #sys.exit()
            if not os.path.exists('commit_files/airflow1/'+cid):
                os.system('mkdir commit_files/airflow1/'+cid)
            os.chdir('airflow/')
            os.system('git show '+cid+'~1:'+f+'> ../commit_files/airflow1/'+cid+'/old_'+newf)
            os.system('git show '+cid+':'+f+'> ../commit_files/airflow1/'+cid+'/new_'+newf)
            os.chdir('../')

            with open('commit_files/airflow1/'+cid+'/old_'+newf) as f1:
                a=f1.read()
            with open('commit_files/airflow1/'+cid+'/new_'+newf) as f2:
                b=f2.read()
            s = difflib.SequenceMatcher(None, a, b)
            changes=[]
            add_line=del_line=t_line=0
            for tag, i1, i2, j1, j2 in s.get_opcodes():
                if tag!='equal':
                    if tag=='delete':
                        dlines=a[i1:i2].count('\n')
                        print('del',dlines)
                        del_line+=dlines
                        t_line+=dlines
                    elif tag=='insert':
                        alines=b[j1:j2].count('\n')
                        print('add',alines)
                        add_line+=alines
                        t_line+=alines
                    cha=(tag, i1, i2, j1, j2, a[i1:i2],b[j1:j2])
                    changes.append(cha)
                    print ('{:7}  a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, a[i1:i2],b[j1:j2]))
                else:
                    print ('{:7}  a[{}:{}] --> b[{}:{}]'.format(tag, i1, i2, j1, j2))
            if len(changes)!=0:
                np.save('commit_files/airflow1/'+cid+'/changes_'+newf+'.npy',changes)
                tryx=np.load('commit_files/airflow1/'+cid+'/changes_'+newf+'.npy')
                print(type(tryx),tryx)
            print(cid,f,add_line,del_line,t_line)
            total_features+=cid+','+f+','+str(add_line)+','+str(del_line)+','+str(t_line)+'\n'
    #sys.exit()
with open('commit_files/ladata/airflow.csv','w+') as f:
    f.write(total_features)
