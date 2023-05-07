#!/usr/bin/env python
# coding: utf-8

import os,re
import json

def print_nodes(path,filename):

    lsdir = os.listdir(path)
    #print(lsdir)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
    #print("---------------")
    #print(dirs)
    if dirs:
        for i in dirs:
            print_nodes(os.path.join(path, i),i)

    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    for f in files:
        #print(os.path.join(path, f))
        #print(f)
        try:
            if f[f.rindex('.'):len(f)] == '.py':
                fullfile = filename + '.' + f
                nodes.append({"name":f,"path":filename+'.'+f})
                tnodes.append(f)
        except:
            print("next")
    print(tnodes)


def print_edges(path,nodes,tnodes):
    print(path)
    print(len(nodes))
    print(len(tnodes))
    e = {"source": -1, "target": -1}
    for n in nodes:
        subpath=n['path'][0:n['path'].rindex('.')]
        print("subpath="+subpath)
        interpath=subpath.replace(".","\\")
        print("interpath="+interpath)
        interpath=interpath+".py"
        print("interpath2="+interpath)
        file = open(os.path.join(path, interpath), 'r', encoding='UTF-8')
        #print(file.read())
        for line in file:
            print(line)
            for ng in nodes:
                modulename=ng['name'][0:-3]
                #print(modulename)
                if (modulename+" " in line) and (('import' in line) or ('from' in line)) and (n!=ng):
                    test = e.copy()
                    test['source'] = (tnodes.index(n['name']))
                    test['target'] = (tnodes.index(ng['name']))
                    links.append(test)
    print(links)



path = r'C:\Python36\Lib\site-packages'
filename='wordcloud'
pynet={"nodes":"","links":""}
nodes=[]
links=[]
tnodes=[]
print_nodes(os.path.join(path, filename),filename)  #生成节点信息
print_edges(path,nodes,tnodes)     #生成边的信息
#写入Json文件
pynet['nodes']=nodes
pynet['links']=links
f = open('../static/netjson/'+filename+'.json', 'w')
f.write(json.dumps(pynet))
f.close()




