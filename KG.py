# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:49:37 2020

@author: 11834
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
import sys

class Entity:
    def __init__(self):
        self.type=None
        self.fathers={} #k,v:[relation name],[entity object]; relation: self [is x relation] of father
        self.children={}  #k,v:[relation name],[entity object]; relation: self [is x relation] of child
        self.father_num=0
        self.children_num=0
        self.node=None # AST node object
        self.id=-1
        self.name=None
        
    def set_node(self,node,type,id,name):
        self.node=node
        self.type=type
        self.id=id
        self.name=name
        
    def add_father(self,father,relation_name):
        if not relation_name in self.fathers:
            tfs=[]
            tfs.append(father)
            self.fathers[relation_name]=tfs
        else:
            tfs=self.fathers[relation_name]
            tfs.append(father)
            self.fathers[relation_name]=tfs
        if not relation_name == None:
            self.father_num+=1
            
    def add_child(self,child,relation_name):
        if not relation_name in self.children:
            tfs=[]
            tfs.append(child)
            self.children[relation_name]=tfs
        else:
            tfs=self.children[relation_name]
            tfs.append(child)
            self.children[relation_name]=tfs
        self.children_num+=1
    
    def print_entity(self):
        
        print("entity name",self.name)
        print("entity id",self.id)
        print("entity type",self.type)
        print("entity node:",self.node)
        print("entity fathers num:",self.father_num)
        print(self.fathers)
        print("entity children num:",self.children_num)
        print(self.children)
        '''
        if self.father_num >0:
            edge=self.fathers.keys()[0]
            nodes=self.fathers.values()[0]
            for node in nodes:
                print(self.id+" "+edge+" "+node.id)
        '''
        
    def get_children(self):
        return self.children
    
    def get_fathers(self):
        return self.fathers
    
    def get_node(self):
        return self.node
    
    def get_id(self):
        return self.id
        
class Relation:
    def __init__(self):
        self.father=None #entity objects
        self.child=None #entity objects
        self.relation_name=None
        
    def set_relation(self,father,child,relation_name):
        self.father=father
        self.child=child
        self.relation_name=relation_name
        

        

class KnowledgeGraph:
    def __init__(self):
        self.relations=[] # from entity1 to entity2, relation objects
        self.entities=[] # entity objects
        self.newe=[]
        self.entity_num=0
        self.relation_num=0
        self.data=""
        self.questions=[]
        
    def add_entity(self,entity):
        self.entities.append(entity)
        self.entity_num+=1
        
    def add_relation(self,relation):
        self.relations.append(relation)
        self.relation_num+=1
        
    def print_kg(self):
        self.update_relations()
        print("entity_num:",self.entity_num)
        for e in self.newe:
            e.print_entity()
        
    def get_entities(self):
        return self.entities
    
    def update_entity(self,e):
        new_entities=[]
        for ie in self.entities:
            if ie.get_node()==e.get_node():
                new_entities.append(e)
            else:
                new_entities.append(ie)
        self.entities=new_entities
        
    def update_relations(self):
        new_entities=[]
        all_entities=self.entities
        for e in all_entities:
            xe=e
            new_fathers={}
            new_children={}
            fathers=e.get_fathers()
            for k,vs in fathers.items():
                new_vs=[]
                for v in vs:
                    for ie in all_entities:
                        ieid=ie.get_id()
                        if ie.node==v and e.get_id()!=ieid:
                            new_vs.append(ieid)
                new_fathers[k]=new_vs
            xe.fathers=new_fathers
            children=e.get_children()
            for k,vs in children.items():
                new_vs=[]
                for v in vs:
                    for ie in all_entities:
                        ieid=ie.get_id()
                        if ie.node==v and e.get_id()!=ieid:
                            new_vs.append(ieid)
                new_children[k]=new_vs
            xe.children=new_children
            new_entities.append(xe)
        self.newe=new_entities
    
    def generare_relations(self):
        #TODO:
        all_entities=self.entities
        for entity in all_entities:
            #entity.print_entity()
            fathers=entity.get_fathers()
            frelations=fathers.keys()
            for frelation in frelations:
                if not frelation in self.relations:
                    self.relations.append(frelation)
                    self.relation_num+=1
                fnodes=fathers[frelation]
                for fnode in fnodes:
                    fentity=None
                    for entityj in all_entities:
                        if entityj.get_node()==fnode and entityj.get_id()!=entity.get_id():
                            fentity=entityj
                            break
                    if fentity!=None:
                        description=str(fentity.get_id())+' '+frelation+' '+str(entity.get_id())
                        print('=='*20)
                        print(description)
                        self.data+=description+'\n'
                        #self.data+='\n'
                    else:
                        print('error')
                        sys.exit()
                        
            children=entity.get_children()
            crelations=children.keys()
            for crelation in crelations:
                if not crelation in self.relations:
                    self.relations.append(crelation)
                    self.relation_num+=1
                cnodes=children[crelation]
                for cnode in cnodes:
                    centity=None
                    for entityj in all_entities:
                        if entityj.get_node()==cnode and entityj.get_id()!=entity.get_id():
                            centity=entityj
                            break
                    if centity!=None:
                        description=str(centity.get_id())+' '+crelation+' '+str(entity.get_id())
                        print('=='*20)
                        print(description)
                        self.data+=description+'\n'
                        #self.data+='\n'
                    else:
                        print('error')
                        sys.exit()
            
        #with open('data.txt','w+') as f:
            #f.write(self.data)
        #sys.exit()
