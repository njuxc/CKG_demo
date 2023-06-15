# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:32:48 2023

@author: 11834
"""

import json
import os,sys
import re
from stanfordcorenlp import StanfordCoreNLP
from twokenize0 import tokenize
from nltk.tokenize import sent_tokenize

def get_sent_tokenize(text):
    snew=text.split('\n')
    sret=[]
    cflag=False
    for st in snew:
        st=st.strip()
        if st=='```':
            if not cflag:
                cflag=True
            else:
                cflag=False
            continue
        if cflag:
            continue
        if st=='':
            continue
        elif re.match('[\'\:\,\(\)\[\]\{\}\.\!\?\<\>\`]+$',st):
            continue
        else:
            sret.extend(sent_tokenize(st))
    return sret


projs=['django', 'scikit-learn','pandas','ansible','airflow','keras']
#projs=['airflow']
label='redundantCall/'
nlp = StanfordCoreNLP(r"/root/corenlp")

for proj in projs:
    dir_name='commit_texts/'+label+proj
    files=os.listdir(dir_name)
    for file in files:
        cid=file.split('.')[0]
        print(cid)
        if not os.path.exists('jsons/'+proj+'/'+cid):
            os.system('mkdir jsons/'+proj+'/'+cid)
        with open(dir_name+'/'+file) as f:
            text=f.read()
        print(text)
        sentence=get_sent_tokenize(text)
        print(sentence)
        #sys.exit()
        id=-1
        for sen in sentence:
            id+=1
            ntext=" ".join(tokenize(sen))
            annot_doc = nlp.annotate(ntext,
            properties={
                'annotators': 'tokenize, ssplit, pos, lemma, ner, regexner,tokensregex',
                'outputFormat': 'json',
                'timeout': 1000,
                'tokenize.whitespace':True,
                'ssplit.eolonly':True,
                'tokensregex.rules':'redundant_dict.txt',
                'outputFormat': 'json'
            })
            #print(annot_doc)
            with open('jsons/'+proj+'/'+cid+'/'+str(id)+'.json','w+') as f:
                f.write(annot_doc)
        #sys.exit()