# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 19:15:39 2023

@author: 11834
"""
import parso
import sys

iter_flag=False

positions = [0]

def find_node(file,sp,ep):
    parsoAst = parso.parse(readFile(file))
    #print(3,parsoAst)
    return processNode(parsoAst,sp,ep)


def processNode(parsoNode,sp,ep):
    if parsoNode.type == 'error_node':
        sys.exit(parsoNode)
    
    ret=toGumtreeNode(parsoNode,sp,ep)
    if ret:
        return ret
    
    for parsoChild in parsoNode.children:
        retChild = toGumtreeNode(parsoChild,sp,ep)
        if retChild != None:
            return retChild
        if hasattr(parsoChild, 'children'):
            tret= processNode(parsoChild,sp,ep)
            if tret:
                return tret

def toGumtreeNode(parsoNode,sp,ep):
    if parsoNode.type in ['keyword', 'newline', 'endmarker']:
        return
    if not parsoNode.type == 'atom_expr':
        return
    if parsoNode.type == 'operator' and parsoNode.value in ['.', '(', ')', '[', ']', ':', ';']:
        return
    startPos = positions[parsoNode.start_pos[0] - 1] + parsoNode.start_pos[1]
    endPos = positions[parsoNode.end_pos[0] - 1] + parsoNode.end_pos[1]
    #print(parsoNode,sp,ep)
    if startPos==sp and endPos==ep:
        return parsoNode
    #length = endPos - startPos
    #if (not hasattr(parsoNode, 'children')) or len(parsoNode.children) == 0:
        #print("label", parsoNode.value)



def readFile(file):
    with open(file, 'r') as file:
        data = file.read()
    index = 0
    for chr in data:
        index += 1
        if chr == '\n':
            global positions
            positions.append(index)
    return data

def extract_call_from_trailer(telements):
    print(5,telements)
    tlen=len(telements)
    i=0
    ret=''
    while i<tlen:
        telement=telements[i]
        if "name: " in telement[1]:
            ret+='.'+telement[1].split(': ')[1]
        elif telement[1]=='atom_expr':
            print('again')
            global iter_flag
            iter_flag=True
            ret+='('+extract_call_from_atom(telements[i:])+')'
            iter_flag=False
            break
        i+=1
    #ret+='##'
    print(6,ret)
    return ret


def extract_call_from_atom(tokens,oldfile):
    #print(1,tokens)
    i=0
    lent=len(tokens)
    filter_code=[]
    while i<lent:
        token=tokens[i]
        if token[1]=='atom_expr':
            i+=1
            elements=[]
            rlevel=token[0]
            sp=token[2]
            ep=token[3]
            while i<lent:
                subtok=tokens[i]
                if subtok[0]>rlevel:
                    elements.append(subtok)
                    i+=1
                else:
                    i-=1
                    break
            elent=len(elements)
            #print(2,elent,sp,ep)
            #sys.exit()
            if elent>0:
                ret=find_node(oldfile,sp,ep)
                if ret:
                    #print(ret.get_code())
                    code=ret.get_code()
                    
                    for cline in code.split('\n'):
                        cline=cline.strip()
                        if cline.startswith('#'):
                            continue
                        filter_code.append(cline)
                    #print(filter_code)
                    #sys.exit()
                #print(1,ret)
                #sys.exit()
        else:
            i+=1
    return filter_code

def extract_call_from_atom0(tokens):
    print(1,tokens)
    i=0
    lent=len(tokens)
    ret=''
    while i<lent:
        token=tokens[i]
        if token[1]=='atom_expr':
            i+=1
            elements=[]
            rlevel=token[0]
            while i<lent:
                subtok=tokens[i]
                if subtok[0]>rlevel:
                    elements.append(subtok)
                    i+=1
                else:
                    i-=1
                    break
            elent=len(elements)
            if elent>0:
                print(2,elements)
                j=0
                while j<elent:
                    etok=elements[j]
                    if 'name: ' in etok[1]:
                        ret+=etok[1].split(': ')[1]
                        print(3, ret)
                        j+=1
                    elif etok[1]=='trailer':
                        k=j+1
                        tlevel=etok[0]
                        telements=[]
                        while k<elent:
                            if elements[k][0]>tlevel:
                                telements.append(elements[k])
                                k+=1
                            else:
                                k-=1
                                break
                        if len(telements)>0:
                            print(3.2,ret)
                            ret+=extract_call_from_trailer(telements)
                            j=k
                            print(4,ret)
                        j+=1
            #ret+='##'
            if not iter_flag:
                ret+='##'
        else:
            
            i+=1

    return ret

def deal_insert_tree(change):
    contexts= change.split('\n---\n')[1]
    lines=contexts.split('\n')
    tokens=[]
    target_level=10000
    for line in lines:
        if line.strip()=='':
            continue
        blank_num=0
        index=0
        while line[index]==' ':
            blank_num+=1
            index+=1
        level=blank_num/4
        token=line[index:].split(' [')[0]
        #print(level,token)
        tokens.append((level,token))
    calls=extract_call_from_atom(tokens)
    sys.exit(0)
    return

def deal_insert_node(change):
    return



def deal_delete_tree(change,oldfile):
    contexts= change.split('\n---\n')[1]
    lines=contexts.split('\n')
    tokens=[]
    target_level=10000
    for line in lines:
        if line.strip()=='':
            continue
        blank_num=0
        index=0
        while line[index]==' ':
            blank_num+=1
            index+=1
        level=blank_num/4
        token=line[index:].split(' [')[0]
        poss=line[index:].split(' [')[1][:-1].split(',')
        sp=int(poss[0])
        ep=int(poss[1])
        lenth=ep-sp
        #print(sp,ep,lenth)
        #print(level,token)
        tokens.append((level,token,sp,ep,lenth))
    calls=extract_call_from_atom(tokens,oldfile)
    #sys.exit(0)
    return calls

def deal_delete_node(change):
    return

def deal_update_node(change):
    return

def deal_move_tree(change):
    return

def readFile(file):
  with open(file, 'r') as file:
    data = file.read()
  index = 0
  for chr in data:
    index += 1
    if chr == '\n':
      positions.append(index)
  return data

def get_code_change(logf,oldfile,newf):

    
    with open(logf,encoding='ISO-8859-1') as f:
        xlines=f.read().strip()
    
    if not ("update-" in xlines or "delete-" in xlines or "insert-" in xlines or "move-" in xlines):
        print('Target file has no change! Failed!')
        sys.exit()
        
    filecs=[]
    changes=xlines.split('===')
    for c in changes:
        if 'match\n---\n' in c:
            continue
        if c.strip()=='':
            continue
        if not 'atom_expr' in c:
            continue
        if 'insert-tree\n---\n' in c:
            continue
            itret=deal_insert_tree(c)
            
        elif 'insert-node\n---\n' in c:
            inret=deal_insert_node(c)
            
        elif 'delete-tree\n---\n' in c:
            filecs.extend(deal_delete_tree(c,oldfile))
            #print(filecs)
            #sys.exit()
        elif 'delete-node\n---\n' in c:
            deal_delete_node(c)
        elif 'update-node\n---\n' in c:
            upret=deal_update_node(c)
            
        elif 'move-tree\n---\n' in c:
            mtret=deal_move_tree(c)
            
    return filecs
                
'''
logf='/root/empirical/extract/commit_files/airflow/116a8a0c67aff3a06e7d66867464555546103b0e/changelog_airflow#utils#dag_processing.py'
oldfile='/root/empirical/extract/commit_files/airflow/116a8a0c67aff3a06e7d66867464555546103b0e/airflow#utils#dag_processing.py'
newf=''

get_code_change(logf,oldfile,newf)
'''