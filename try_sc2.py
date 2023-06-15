# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:58:30 2023

@author: 11834
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:39:30 2022

@author: 11834
"""

from tqdm import tqdm
import binascii
from git import Repo
import os,sys


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
error=success=0

for commit in tqdm(commits):
    cid=binascii.b2a_hex(commit.binsha).decode("utf-8")
    if not cid in tcommits:
        continue
    #target_dir='data/airflow/'+cid
    #if not os.path.exists(target_dir):
        #os.makedirs(target_dir)
    
    files=commit.stats.files.keys()
    for f in files:
        if f.endswith('.py'):
            #print('commit files:'+str(commit.stats.files)+'\n')
            #sys.exit()
            newf=f.replace('/','#')
            print(f,newf)
            #sys.exit()
            if not os.path.exists('commit_files/airflow/'+cid):
                os.system('mkdir commit_files/airflow/'+cid)
            os.chdir('airflow/')
            os.system('git show '+cid+'~1:'+f+'> ../commit_files/airflow/'+cid+'/'+newf)
            os.system('git show '+cid+':'+f+'> ../commit_files/airflow/'+cid+'/new_'+newf)
            fa='../commit_files/airflow/'+cid+'/'+newf
            fb='../commit_files/airflow/'+cid+'/new_'+newf
            logf= '../commit_files/airflow/'+cid+'/changelog_'+newf
            os.system('gumtree textdiff '+'../commit_files/airflow/'+cid+'/'+newf+' ../commit_files/airflow/'+cid+'/new_'+newf+' > '+logf)
            
            with open(logf,encoding='ISO-8859-1') as f:
                xlines=f.read()
                xlines=xlines.strip()
                if xlines=='':
                    os.system('rm '+logf)
                    error+=1
                    continue
                else:
                    success+=1
                print(error,success)
            
            if not ("update-" in xlines or "delete-" in xlines or "insert-" in xlines or "move-" in xlines):
                    kind=filea=fileb=''
                    os.system('rm '+logf+' '+fa+' '+fb)
                    continue
                
            os.chdir('../')
            #sys.exit()
