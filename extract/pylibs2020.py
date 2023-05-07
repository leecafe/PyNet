#!/usr/bin/env python
# coding: utf-8
#变量没有清空，需要重新开始，否则容易重复写入pylibs
# In[5]:

#先执行pip3 list >>pylibs.txt   所有的第三方包的名称和版本，再对每一个包提取它的require, 和required
import json

netjson = {"links": "", "nodes": ""}
nodejson = []
edgejson = []
pylibs = []

e = {"source": -1, "target": -1}

def requires(libname):
    import os
    print(libname)
    #re=os.popen(r'c:\python36\scripts\pip3 show flask').read()
    re=os.popen(r'c:\python36\scripts\pip3 show '+libname).read()
    relist=[]
    relist=re.split('\n')
    require=relist[8]
    required=relist[9]
    requirelist=[]
    requiredlist=[]
    requirelist=require[require.find(':')+2:].split(', ')
    #print(requirelist)
    requiredlist=required[required.find(':')+2:].split(', ')
    #print(requiredlist)
    return requirelist,requiredlist


# In[3]:

def readpylibs():
    filename='../static/pylibs.txt'
    i=0
    with open(filename,'r',encoding='utf-8') as f:
        #line=f.readline()
        line=f.readline()
        while(line):
            #print(line)

            pylibs.append(line.split(" ")[0])
            line = f.readline()
            i=i+1
        print(i)
    #print(pylibs)
    pylibs.pop()
    print(pylibs)
    return pylibs


# In[12]:


#---json格式的网络文件



#节点

def nodes(pylibs):
    for n in pylibs:
        #print(n)
        d = {"name": ""}
        d['name']=n
        #print(d)
        nodejson.append(d)
        #print(nodejson)
    netjson['nodes']=nodejson
    return len(nodejson)

#边的关系
def edges(pylibs):
    print(pylibs)
    for n in pylibs:
        print('--------------------------------------------')
        print(n)
        requirelist,requiredlist=requires(n)

        print(requirelist)
        print(requiredlist)

        i=0
        if not(len(requirelist)==1 and requirelist[0]==''):
            for eg in requirelist:
                test=e.copy()
                test['source']=(pylibs.index(n))
                if not(eg in pylibs):
                    pylibs.append(eg)
                test['target']=(pylibs.index(eg))
                edgejson.append(test)
                i=i+1
            netjson['links']=edgejson
    return len(edgejson)



#写入Json文件
if __name__=='__main__':
    f = open('../static/netjson/pylibs.json', 'w',encoding='utf-8')
    netjson = {"links": "", "nodes": ""}
    nodejson = []
    edgejson = []
    pylibs = []
    pylibs=readpylibs()
    #print(pylibs)
    edges(pylibs)
    nodes(pylibs)
    f.write(json.dumps(netjson))
    f.close()


# In[ ]:




