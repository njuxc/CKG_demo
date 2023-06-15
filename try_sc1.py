#['match', 'insert-tree', 'delete-tree', 'insert-node', 'delete-node', 'move-tree', 'update-node']

import os,sys,json

def get_file_path(root_path,file_list,dir_list):
    dir_or_files = os.listdir(root_path)
    #print 1,dir_or_files
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root_path,dir_file)
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)
    #print 3,file_list
    return file_list
    
def GetMiddleStr(content,startStr,endStr):
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
        endIndex = content.index(endStr)
    return content[startIndex:endIndex]
    
#TODO:Extract candidates
def deal_insert_tree(c):
    #print(c)
    ret=[]
    ret1=[]
    try:
        change=GetMiddleStr(c,'---\n',']\nto\n').strip()
    except Exception as err:
        print(err)
        print(c)
        return []
    #print(change)
    cs=change.split(']\n')
    #print(cs)
    for ic in cs:
        ic=ic.strip()
        if ic=='':
            continue
        pindex=ic.rfind(' [')
        pos=ic[pindex+1:]+']'
        #print(pos)
        preinfo=ic[:pindex]
        if ': ' in preinfo:
            findex=preinfo.find(': ')
            node=preinfo[:findex]
            label=preinfo[findex+2:].strip()
        else:
            node=preinfo.strip()
            label='null'
        #print(node,label)
        ret.append(('add',node,label))
        ret1.append((('add',node,label),pos))
    '''
    calls=[]
    attrloads=[]
    attrs=[]
    for cs in ret1:
    #print(cs[0])
        if cs[0][1]=='Call':
            calls.append(cs)
        elif cs[0][1]=='AttributeLoad':
            attrloads.append(cs)
        elif cs[0][1]=='attr':
            attrs.append(cs)
    '''
    #if len(calls)>0 and len(attrloads)>0 and len(attrs)>0:
        #global candidates
        #for attr in attrs:
            #candidates.add(attr[0][2])
    return ret
    #sys.exit(0)
    
def deal_move_tree(c):
    #print(c)
    ret=[]
    try:
        change=GetMiddleStr(c,'---\n',']\nto\n').strip()
    except Exception as err:
        print(err)
        print(c)
        return []
    #print(change)
    cs=change.split(']\n')
    #print(cs)
    for ic in cs:
        ic=ic.strip()
        if ic=='':
            continue
        pindex=ic.rfind(' [')
        pos=ic[pindex+1:]+']'
        #print(pos)
        preinfo=ic[:pindex]
        if ': ' in preinfo:
            findex=preinfo.find(': ')
            node=preinfo[:findex]
            label=preinfo[findex+2:].strip()
        else:
            node=preinfo.strip()
            label='null'
        #print(node,label)
        ret.append(('move',node,label))
    #print(ret)
    return ret
    

def deal_delete_tree(c):
    #print(c)
    ret=[]
    change=c.split('---\n')[1].strip()[:-1]
    #print(change)
    #sys.exit()
    cs=change.split(']\n')
    for ic in cs:
        ic=ic.strip()
        if ic=='':
            continue
        pindex=ic.rfind(' [')
        pos=ic[pindex+1:]+']'
        #print(pos)
        preinfo=ic[:pindex]
        if ': ' in preinfo:
            findex=preinfo.find(': ')
            node=preinfo[:findex]
            label=preinfo[findex+2:].strip()
        else:
            node=preinfo.strip()
            label='null'
        #print(node,label)
        ret.append(('delete',node,label))
    #print(ret)
    #sys.exit()
    return ret
    
def deal_delete_node(c):
    #print(c)
    ret=[]
    change=c.split('---\n')[1].strip()
    #print(change)
    #sys.exit()
    ic=change
    pindex=ic.rfind(' [')
    pos=ic[pindex+1:]
    #print(pos)
    preinfo=ic[:pindex]
    if ': ' in preinfo:
        findex=preinfo.find(': ')
        node=preinfo[:findex]
        label=preinfo[findex+2:].strip()
    else:
        node=preinfo.strip()
        label='null'
    ret.append(('delete',node,label))
    #print(ret)
    return ret
    
    
def deal_insert_node(c):
    #print(c)
    ret=[]
    try:
        change=GetMiddleStr(c,'---\n',']\nto\n')
    except Exception as err:
        print(err)
        print(c)
        return []
    ic=change.strip()+']'
    pindex=ic.rfind(' [')
    pos=ic[pindex+1:]
    #print(pos)
    preinfo=ic[:pindex]
    if ': ' in preinfo:
        findex=preinfo.find(': ')
        node=preinfo[:findex]
        label=preinfo[findex+2:].strip()
    else:
        node=preinfo.strip()
        label='null'
    ret.append(('add',node,label))
    #print(ret)
    return ret

def deal_update_node(c):
    #print(c)
    ret=[]
    try:
        change=GetMiddleStr(c,'---\n',']\nreplace')
    except Exception as err:
        print(err)
        print(c)
        return []
    ic=change.strip()+']'
    pindex=ic.rfind(' [')
    pos=ic[pindex+1:]
    #print(pos)
    preinfo=ic[:pindex]
    if ': ' in preinfo:
        findex=preinfo.find(': ')
        node=preinfo[:findex]
        label=preinfo[findex+2:].strip()
    else:
        node=preinfo.strip()
        label='null'
    ret.append(('update',node,label))
    #print(ret)
    return ret
    
    
            
rootdir='/root/empirical/data/'
projs=os.listdir(rootdir)
print(projs)
cans=[]

filenums={}
slocs={}
sizes={}
commitnums={}
changedfiles={}
allastnodes={}
changedastnodes={}
changenums={}
changedAPIs={}

for proj in projs:
    print(proj)
    CURRENT_PROJ=proj
    with open(CURRENT_PROJ+'.csv') as f:
        tlines=f.readlines()
    
    tcommits=[]

    for tiline in tlines:
        tiline = tiline.strip()
        tcommits.append(tiline)
    print(tcommits)

    os.system('mkdir /root/empirical/logs/log_'+CURRENT_PROJ)
    os.system('mkdir /root/empirical/cts/'+CURRENT_PROJ)
    os.system('mkdir /root/empirical/Tmp/'+CURRENT_PROJ)
    os.system('mkdir /root/empirical/changes/'+CURRENT_PROJ)
    os.chdir(rootdir+proj)
    
    os.system('git log -p --reverse --  \'*.py\' > /root/empirical/slogs/'+CURRENT_PROJ+'_log.txt')
    with open('/root/empirical/slogs/'+CURRENT_PROJ+'_log.txt',encoding='ISO-8859-1') as f:
        lines=f.readlines()

    commit=''
    kind=''
    filea=''
    fileb=''
    num=0
    idd=0
    commit_cs=''
    error=0
    success=0
    candidates=[]
    tnum=0
    count=0
    
    commitnum=0
    filenum=0
    sloc=0
    size=0
    changedfile=0
    allastnode=0
    changedastnode=0
    changenum=0
    changedAPI=0
    #fnum=-1
    pre_dir=''
    for line in lines:
        #line=lines[li].strip()
        #print('start',line)
        ls=line.split(' ')
        if 'commit' in line and len(ls)==2:
            #print(1)
            whole_cs=[]
            gcommit=ls[1]
            print(gcommit)
            num=num+1
        
            if num == 1:
                os.chdir('/root/empirical/data/'+CURRENT_PROJ)
                os.system('git reset --hard '+gcommit)
            else:
                os.system('rm -r /root/empirical/Tmp/'+CURRENT_PROJ)
                #os.system('mkdir train_/root/empirical/Tmp/'+str(num))
                os.system('cp -r /root/empirical/data/'+CURRENT_PROJ+' /root/empirical/Tmp/'+CURRENT_PROJ)
                #os.system('cp -r /root/empirical/data2/+CURRENT_PROJ+' train_/root/empirical/Tmp/'+str(num))
                os.chdir('/root/empirical/data/'+CURRENT_PROJ)
                os.system('git reset --hard '+gcommit)

        elif 'index' in line and len(ls)==3:
            #print(2)
            kind=line
        elif '--- a' in line and kind!='':
            #print(3)
            filea=ls[1][1:-1]
        elif '--- /' in line:
            #print(4)
            filea=ls[1][:-1]
        elif '+++ b' in line and kind!='':
            #print(5)
            fileb=ls[1][1:-1]
            print(filea,fileb)
            if not filea==fileb:
                continue
            if filea.endswith('setup.py'):
                continue
            if not gcommit in tcommits:
                continue
            #print commit
            print('hint!')
            sys.exit()
            if num > 1:
                idd+=1
                
                #os.chdir('/root/empirical/gumtree/dist/build/distributions/gumtree-2.1.3-SNAPSHOT/bin')
                #os.system('ls')
                #print num
                #print commit,kind,filea,fileb
                fa='/root/empirical/data/'+CURRENT_PROJ+fileb
                fb='/root/empirical/Tmp/'+CURRENT_PROJ+filea
                logf='/root/empirical/logs/log_'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd)
                print(fa,fb,logf)
                os.system('gumtree textdiff '+fa+' '+fb+' > '+logf)
                #print('succ1')
                #sys.exit()
                whole_cs=[]
                with open(logf,encoding='ISO-8859-1') as f:
                    xlines=f.read()
                if xlines.strip()=='':
                    os.system('rm '+logf)
                    error+=1
                    continue
                else:
                    success+=1
                print(error,success)
                xlines=xlines.strip()
                #print(lines)
                #sys.exit()
            
                if not ("update-" in xlines or "delete-" in xlines or "insert-" in xlines or "move-" in xlines):
                    #print(1)
                    #with open('/root/empirical/logs/log_'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd)) as f:
                        #f.write(lines)
                    kind=filea=fileb=''
                    os.system('rm /root/empirical/logs/log_'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd))
                    continue
                #print('succ2')
                #sys.exit()
                #changedfile=changedfile+1
                #print('changedfile',changedfile)
                    
                #os.system('gumtree parse /root/empirical/Tmp/'+CURRENT_PROJ+filea+' > /root/empirical/logs/ast_cur.json')
                #with open('/root/empirical/logs/ast_cur.json',encoding='ISO-8859-1') as f:
                        #curlines=f.readlines()
                #allastnode=allastnode+len(curlines)
                #print('allastnode',allastnode)

                filecs=[]
                changes=xlines.split('===')
                for c in changes:
                    if 'match\n---\n' in c:
                        continue
                    if c.strip()=='':
                        continue
                    #if 'Call' in c and 'AttributeLoad' in c and 'attr' in c:
                    if 'Call' in c:
                        changedAPI=changedAPI+1
                        print('changedAPI',changedAPI)
                    else:
                        continue
                    if 'insert-tree\n---\n' in c:
                        itret=deal_insert_tree(c)
                        if len(itret)>0:
                            filecs.extend(itret)
                    elif 'insert-node\n---\n' in c:
                        inret=deal_insert_node(c)
                        if len(inret)>0:
                            filecs.extend(inret)
                    elif 'delete-tree\n---\n' in c:
                        filecs.extend(deal_delete_tree(c))
                    elif 'delete-node\n---\n' in c:
                        filecs.extend(deal_delete_node(c))
                    elif 'update-node\n---\n' in c:
                        upret=deal_update_node(c)
                        if len(upret)>0:
                            filecs.extend(upret)
                    elif 'move-tree\n---\n' in c:
                        mtret=deal_move_tree(c)
                        if len(mtret)>0:
                            filecs.extend(mtret)
                    
                    #changenum=changenum+1
                    #print('changenum',changenum)
                    
                #print('succ3')
                #changedastnode=changedastnode+len(filecs)
                #print('changedastnode',changedastnode)
                #print(filecs)
                #sys.exit()
                if len(filecs)>0:
                    #fnum+=1
                    csjson=json.dumps(filecs)
                    ctsfile='/root/empirical/cts/'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd)
                    with open(ctsfile,'w+') as f1:
                        f1.write(csjson)
                    #print(1)
                    os.system('mkdir /root/empirical/changes/'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd))
                    os.system('cp '+fb+' /root/empirical/changes/'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd)+'/old.py')
                    os.system('cp '+fa+' /root/empirical/changes/'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd)+'/new.py')
                    with open('/root/empirical/changes/'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd)+'/name.txt','w+') as ff:
                        ff.write(gcommit+'\n'+filea)
                    #sys.exit()
                else:
                    os.system('rm /root/empirical/logs/log_'+CURRENT_PROJ+'/'+str(num)+'_'+str(idd))
        #print(5,len(lines))
    sys.exit()
