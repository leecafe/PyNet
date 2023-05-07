import bs4
import bs4.tests
import inspect
import json
import jieba
import py2neo
import numpy
import flask
from flask import Flask
import wordcloud
import dlib
import networkx
import nltk
import PIL
import pandas
import matplotlib
from matplotlib import pyplot
import torch
import facenet_pytorch



modules = []
mnetjson = {'nodes': '', 'links': ''}
nodes = []
links = []
myclass = ""
myfunction = ""

layer=0
def get_modules(arg,str,layer):
    if arg.__name__ == filename:
        modules.append(arg.__name__)
        hasclass=inspect.getmembers(arg, inspect.isclass)
        hasfunction=inspect.getmembers(arg, inspect.isfunction)
        # print("Function-------")
        # print(hasfunction)
        myclass=""
        classcount=0
        for h in hasclass:
            if h[1].__module__==arg.__name__:
                #myclass=myclass+h[1].__module__+"."+h[1].__name__+";"
                myclass = myclass + h[1].__name__ + ";"
                classcount=classcount+1;

        myfunction=""
        functioncount=0
        for f in hasfunction:
            if f[1].__module__==arg.__name__:
                myfunction = myfunction + f[1].__name__ + ";"
                functioncount=functioncount+1;
        nodes.append({'name': arg.__name__, 'file': arg.__file__,'layer':layer,'hasclass':classcount,'myclass':myclass,"hasfunction":functioncount,"myfunction":myfunction})
    mmembers = inspect.getmembers(arg, inspect.ismodule)
    layer = layer + 1
    # print(mmembers)
    # print('--------------------------')
    for (name, moduleurl) in mmembers:
        #print("name="+name)
        #print(moduleurl.__name__)
        if str in moduleurl.__name__ and not(moduleurl.__name__ in modules):
            modules.append(moduleurl.__name__)
            mname = arg.__name__ + "." + name
            #modules.append(mname)
            #print(modules)

            # print(mname)
            if '__file__' in dir(eval(mname)):
                # print(eval(mname).__file__)
                hasclass = inspect.getmembers(eval(mname), inspect.isclass)
                hasfunction = inspect.getmembers(eval(mname), inspect.isfunction)
                # print(mname+"=---Function--------------")
                # print(hasfunction)
                myclass=""
                classcount=0
                for h in hasclass:
                    if h[1].__module__ == mname:
                        #myclass=myclass+h[1].__module__+"."+h[1].__name__+";"
                        myclass = myclass + h[1].__name__ + ";"
                        classcount=classcount+1;

                myfunction = ""
                functioncount = 0
                for f in hasfunction:
                    if f[1].__module__ == mname:
                        myfunction = myfunction + f[1].__name__ + ";"
                        functioncount = functioncount + 1;

                nodes.append({'name': moduleurl.__name__, 'file': eval(mname).__file__,'layer':layer,'hasclass':classcount,'myclass':myclass,"hasfunction":functioncount,"myfunction":myfunction})
                #             print()
                #             print('-----------')
                #             print(mname)
                get_modules(eval(mname),filename,layer)
    return modules



def get_links(mymodule,str):
    for m in mymodule:
        nextmodules = []
        #print(m)
        mm = inspect.getmembers(eval(m), inspect.ismodule)
        #print(mm)
        #print('--------------------------')
        for (name, moduleurl) in mm:
            if str in moduleurl.__name__:
                nextmodules.append(moduleurl.__name__)
        count = len(nextmodules)
        leavesmodules = []
        flagin=0
        flagout=0
        leavesmodules,flagout = delfather(m,nextmodules,flagin)
        #print(leavesmodules)
        if (count==0) or (len(leavesmodules)>0) or (len(leavesmodules)==0 and flagout==1):   #叶子节点（没有引用外部模块）或者没有remove完所有的引用模块
            links.append({'name': m, 'size':len(nextmodules),'imports' :nextmodules})

    print(links)
    return links


def delfather(str,modulelist,flag):
    for mo in modulelist:
        #print(mo)
        #print(str, mo[0:len(str)])
        if mo[0:len(str)] == str:
            modulelist.remove(mo)
            delfather(str,modulelist,flag)
        if str[0:len(mo)] == mo:
            modulelist.remove(mo)
            delfather(str, modulelist,flag)
            flag = 1
    return modulelist,flag

def netjson(filename):
    #递归搜索模块Module节点

    mymodule = get_modules(eval(filename),filename,layer)
    print(mymodule)
    print("----")

    print(len(nodes))

    # filename = 'matplotlib.pyplot'
    # mymodule = get_modules(eval(filename), filename)
    # print("----------------------!")
    # print(len(nodes))

    get_links(mymodule,filename)

    #mnetjson['nodes'] = nodes
    mnetjson['links'] = links

    #print(mnetjson)
    print('----end----')

    f = open('../static/treenet/'+filename+'.json', 'w')
    f.write(json.dumps(links))
    f.close()

path = r'C:\Python36\Lib\site-packages'
filename = 'numpy'
# #
netjson(filename)
