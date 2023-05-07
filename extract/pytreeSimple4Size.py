#!/usr/bin/env python
# coding: utf-8
#过滤掉__pycache__
'''
import os
print(os.getcwd())
os.chdir(r'c:\python36')
re=os.popen(r'dir').read()
print(re)
'''

import os
import json




def print_files(path,tree):
    
    child=[]
    lsdir = os.listdir(path)

    for f in lsdir:
        if f!='__pycache__':
            if os.path.isfile(os.path.join(path, f)):
                fsize=os.path.getsize(os.path.join(path, f))
                child.append({"name":""+f+"","value":fsize})
            else:
                child.append({"name": "" + f + ""})
    print(lsdir)
    tree['children']=child
    
    print(tree)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    print("---------------")
    print(dirs)
    if dirs:
        for i in dirs:           
            subtree={"name":"","children":""}            
            #print(subtree)
            print(i)
            for t in tree['children']:
                if t['name']==i:
                    print(t,t['name'])
                    subtree=t
            print(subtree)
            print_files(os.path.join(path, i),subtree)
    files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
    for f in files:
        print(os.path.join(path, f))



path=r'C:\Python36\Lib\site-packages\open3d'
#path=r'C:\Python36'
filename=path[path.rindex('\\')+1:len(path)]
pytree={"name":filename,"children":""}
print_files(path,pytree)
#写入Json文件
f = open('../static/treejson/'+filename+'.json', 'w')
f.write(json.dumps(pytree))
f.close()




