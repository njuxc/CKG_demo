       # -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 13:32:57 2020

@author: 11834
"""



import ast
from ASTVisitor import ASTVisitor


def parseAST(file):
    
    with open(file) as f:
        src=f.read()
        
    asttree=ast.parse(src,file)
    print(ast.dump(asttree))
    visitor=ASTVisitor()
    visitor.visit(asttree)
    visitor.print_ques()
    visitor.print_kg()
    visitor.generare_relations()
    
parseAST('data/airflow/airflow/plugins_manager.py')

#parseAST("test.py")