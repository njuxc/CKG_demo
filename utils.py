# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:01:59 2020

@author: 11834
"""

import ast
import sys

def get_node_value(node, live_obj=None):
    #print ast.dump(node)
    #print "in ASTUtils get_node_value"
    original_node=node
    node_val = []
    try:
        while node != "":
            if isinstance(node, ast.Name):
                #print live_obj,node.id, node.id in live_obj.keys()
                if live_obj:
                    suffix=".".join(node_val)
                    if node.id in live_obj.keys():
                        node_val=[]
                        for val in live_obj[node.id]:
                            node_val += [val+"."+suffix]
                    else:
                        node_val = [node.id] + node_val
                else:
                    node_val = [node.id] + node_val
                break
            elif isinstance(node, ast.Tuple) or \
                    isinstance(node, ast.List):
                t_val=[]
                for t in node.elts:
                    t_val.append('.'.join(get_node_value(t)))
                node_val=[','.join(t_val)]+node_val
                break
            elif isinstance(node, ast.Attribute):
                node_val = [node.attr] + node_val
                node = node.value
            elif isinstance(node, ast.Call):
                node = node.func
            elif isinstance(node, ast.Subscript):
                node_value=node_val
                node_val=get_node_value(node.value)
                if node_val:
                    node_val[-1]+='['+'.'.join(get_node_value(node.slice))+']'
                node_val+=node_value
                break
            elif isinstance(node, ast.Index):
                if isinstance(node.value, ast.Str):
                    node_val=["'"+node.value.s+"'"]
                elif isinstance(node.value, ast.Num):
                    node_val=[str(node.value.n)]
                break
            else:
                break
    except:
        print(sys.exc_info())
        print(ast.dump(original_node))
    return node_val