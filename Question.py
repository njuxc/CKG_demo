# -*- coding: utf-8 -*-
"""
Created on Fri May 21 15:17:43 2021

@author: 11834
"""

#This is a simple extension framework entry for the later processing of GGNN construction.

class Question:
    def __init__(self):
        self.id=-1
        self.question=None
        self.answer=-1
        
    
    def generate(self,id,nodeA,relation,nodeB,answer):
        self.id=id
        self.question=(nodeA,relation,nodeB)
        self.answer=answer
        
    def print(self):
        print("Question "+str(self.id)+": "+str(self.question)+"? "+str(self.answer))