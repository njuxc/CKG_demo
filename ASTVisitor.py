#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:52:32 2020

@author: xincheng
"""

'''
There are five kinds of code entity types: class,
property, method, parameter and variable; and five relation types
in code knowledge graph: "inheritance"(between class and class),
"has"(between class and property, class and method, method and
parameter, method and variable), "instance_of" (between property
and class, variable and class), "return_type" (between method and
class) and "call" (between method and method).
'''

import ast
import sys
from KG import Entity,Relation,KnowledgeGraph
from utils import get_node_value
from Question import Question

class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        #print('ast visiting start!')
        self.kg=KnowledgeGraph()
        self.nid=-1
        self.parent_node=(None,None) # father,relation_name
        self.relation=None
        self.last_node=None
        self.question=None
        self.questions=[]
        self.quesno=-1
        
       
        
        
    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        #if method=="visit_ClassDef":
            #self.extract_ClassDef(node)
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    
    def visit_ClassDef(self, node):
        entity= Entity()
        self.nid+=1
        entity.set_node(node,"Class",self.nid,node.name)

        #for deco in node.decorator_list:
            #entity.add_child(deco,"is_deco_of")
        
        #self.maybe_newline()
        for deco in node.decorator_list:
            #self.fill("@")
            self.visit(deco)
            
        #self.fill("class " + node.name)
        
        comma = False
        #Dealing with class inheritance
        for e in node.bases:
            self.relation="is_inherited_from"
            self.last_node=node
            entity.add_father(e,"is_fatherclass_of")
            self.visit(e)
        self.relation=None
        self.last_node=None
        
        for e in node.keywords:
            self.visit(e)
        
        #Dealing with class has

        for e in node.body:
            #class and property
            if isinstance(e,ast.Assign):
                entity.add_child(e,"is_property_of")
                self.relation="is_class_of"
                self.last_node=node
                self.visit(e)
                self.relation=None
                self.last_node=None
            #class and method,class and variable
            elif isinstance(e,ast.FunctionDef):
                entity.add_child(e,"is_method_of")
                self.relation="is_class_of"
                self.last_node=node
                self.visit(e)
                self.relation=None
                self.last_node=None
                #这里本打算重复遍历e，建立class和var的关系
                #暂时先不做，因为method已经带var了，之后可以二次遍历method，
                #在class和var的点之前连线
            else:
                self.visit(e)
        
        #Deal with has of class and variable
        #在这里遍历method，建立与var的连线.method是中介，要遍历var entity
        '''
        for e in self.kg.get_entities():
            if e.type!="Method":
                continue
            fathers=e.get_fathers()
            if "is_class_of" in fathers:
                if node in fathers["is_class_of"]:
                    print("find method!")
                    varss=e.get_children()["is_variable_of"]
                    for var in varss:
                        entity.add_child(var,"is_variable_of")
        '''
        if "is_method_of" in entity.get_children():
            methods=entity.get_children()["is_method_of"]
            for e in self.kg.get_entities():
                if e.type!="Variable":
                    continue
                fathers=e.get_fathers()
                if "is_method_of" in fathers:
                    ms = fathers["is_method_of"]
                    for m in methods:
                        if m in ms:
                            #print("yes")
                            #print(e.get_node().id)
                            entity.add_child(e.get_node(),"is_variable_of")
                            e.add_father(node,"is_class_of")
                            self.kg.update_entity(e)
        
            
        
        #Add entity to KG
        #entity.print_entity()
        self.kg.add_entity(entity)
        #self.kg.print_kg()
        #self.relation=None
        #self.last_node=None
    
    
    def visit_Name(self,node):

        #Dealing with class inheritance
        if self.relation=="is_inherited_from" and self.last_node!=None:
            entity= Entity()
            self.nid+=1
            entity.set_node(node,"Class",self.nid,node.id)
            #print(node.id)
            entity.add_child(self.last_node,"is_childclass_of")
            #entity.print_entity()
            self.kg.add_entity(entity)
            #self.kg.print_kg()
            #self.relation=None
            #self.last_node=None
        elif self.relation=="is_method_of" and self.last_node!=None:
            #print(1)
            #print(ast.dump(node))
            entity= Entity()
            self.nid+=1
            entity.set_node(node,"Variable",self.nid,node.id)
            #print(node.id)
            entity.add_father(self.last_node,"is_method_of")
            #entity.print_entity()
            self.kg.add_entity(entity)
            #self.kg.print_kg()
            #self.relation=None
            #self.last_node=None 
        #else:
            #entity= Entity()
            #self.nid+=1
            #entity.set_node(node,"Variable",self.nid,node.id)
            
    def visit_Call(self,node):
        self.question="visit_call"
        self.visit(node.func)
        self.question=None
        for e in node.args:
            self.visit(e)
        for e in node.keywords:
            self.visit(e)
            
    def visit_Attribute(self,node):
        
        if self.relation=="is_inherited_from" and self.last_node!=None:
            attr_name=".".join(get_node_value(node.value))
            #print("attr")
            #print(attr_name)
            entity= Entity()
            self.nid+=1
            entity.set_node(node,"Class",self.nid,attr_name+"."+node.attr)
            #print(node.attr)
            entity.add_child(self.last_node,"is_childclass_of")
            #entity.print_entity()
            self.kg.add_entity(entity)
            #self.kg.print_kg()
            #self.relation=None
            #self.last_node=None
        if self.question=="visit_call":
            call_name=".".join(get_node_value(node.value))
            #print('API Invoation Point')
            #print(call_name)
            api_name=node.attr
            #print(api_name)
            self.quesno+=1
            ques=Question()
            ques.generate(self.quesno,call_name,"invoke",api_name,1)
            self.questions.append(ques)
            #ques.print()
            self.question=None
            
        
        
        self.visit(node.value)

            
    def visit_Assign(self,node):
        if self.relation=="is_class_of" and self.last_node!=None:
            entity= Entity()
            self.nid+=1
            entity.set_node(node,"Property",self.nid,"varnode")
            entity.add_father(self.last_node,"is_class_of")
            #entity.print_entity()
            self.kg.add_entity(entity)
            #self.kg.print_kg()
            #self.relation=None
            #self.last_node=None
        for target in node.targets:
            self.visit(target)
        self.visit(node.value)
            
    def visit_FunctionDef(self,node):
        print(ast.dump(node))
        is_connected=0
        entity= Entity()
        self.nid+=1
        entity.set_node(node,"Method",self.nid,node.name)

        if self.relation=="is_class_of" and self.last_node!=None:
            is_connected=1
            entity.add_father(self.last_node,"is_class_of")
            self.relation=None
            self.last_node=None
            
        for deco in node.decorator_list:
            self.visit(deco)


        argss=node.args
        #Here,we only deal with normal parameter
        #all_args = argss.posonlyargs + argss.args
        all_args = argss.args

        #Deal with "has" of method and parameter
        if len(all_args)>0:
            is_connected=1
            for arg in all_args:
                self.relation="is_method_of"
                self.last_node=node
                entity.add_child(arg,"is_parameter_of")
                self.visit(arg)
                self.relation=None
                self.last_node=None

        if node.returns:
            #is_connected=1
            self.visit(node.returns)
            
        #Deal with  "has" of method and variable && method and method
        for e in node.body:
            #这里先只add child entity，结束后反遍历child entity，把father entity的关系加上

            if e.__class__.__name__=='Return':
                self.relation="is_method_of"
                self.last_node=node
                entity.add_child(e,"is_returnvar_of")
                self.visit(e)
                self.relation=None
                self.last_node=None
            else:
                self.relation="is_method_of"
                self.last_node=node
                self.visit(e)
                self.relation=None
                self.last_node=None
            
        #根据child entity反遍历补充father entity信息
        for e in self.kg.get_entities():
            #print(e)
            if not e.type=="Variable":
                continue
            fathers=e.get_fathers()
            #print(fathers)
            if "is_method_of" in fathers:
                for father in  fathers["is_method_of"]:
                    if father==node:
                        #print("yes")
                        is_connected=1
                        entity.add_child(e.get_node(),"is_variable_of")
                        
        # method and method
        #TODO:
        
            
        if is_connected:
            #entity.print_entity()
            self.kg.add_entity(entity)
        self.relation=None
        self.last_node=None
           

    def visit_arg(self, node):
        #print("in vargs")
        if self.relation=="is_method_of" and self.last_node!=None:
            entity= Entity()
            self.nid+=1
            entity.set_node(node,"Parameter",self.nid,node.arg)
            entity.add_father(self.last_node,"is_method_of")
            #entity.print_entity()
            self.kg.add_entity(entity)
            #self.kg.print_kg()
            #self.relation=None
            #self.last_node=None
            
    def visit_Return(self,node):
        if self.relation=="is_method_of" and self.last_node!=None:
            entity= Entity()
            self.nid+=1
            entity.set_node(node,"Returnvar",self.nid,'.'.join(get_node_value(node.value)))
            entity.add_father(self.last_node,"is_method_of")
            #entity.print_entity()
            self.kg.add_entity(entity)
            #self.kg.print_kg()
            #self.relation=None
            #self.last_node=None
            
    def print_kg(self):
        self.kg.print_kg()

    def generare_relations(self):
        self.kg.generare_relations()
    
    def print_ques(self):
        for ques in self.questions:
            ques.print()