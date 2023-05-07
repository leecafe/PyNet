#剔除了Open3D里的没有文件对应问题（Nodes）
#剔除了NLTK里别名和重定向问题（Nodes）
import bs4
import bs4.tests
import inspect
import json
import werkzeug
#import py2neo
import jieba
import numpy
import flask
from flask import Flask
import wordcloud
import dlib
import networkx
import nltk
import open3d
import PIL
import pandas
import matplotlib
from matplotlib import pyplot
import torch
import facenet_pytorch
import pylint
from pylint import pyreverse
import open3d
import vtk
import vtkmodules
import scipy
import torchvision


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
        print("Function-------")
        print(hasfunction)
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
    print(mmembers)
    print('--------------------------')
    for (name, moduleurl) in mmembers:
        # print("name="+name)
        # print(moduleurl.__name__)
        if str in moduleurl.__name__ and not(moduleurl.__name__ in modules):
            modules.append(moduleurl.__name__)
            mname = arg.__name__ + "." + name
            #modules.append(mname)
            #print(modules)

            # print(mname)
            if ('__file__' in dir(eval(moduleurl.__name__)))or(len(inspect.getmembers(arg, inspect.ismodule))>0):
                # print(eval(mname).__file__)
                hasclass = inspect.getmembers(eval(moduleurl.__name__), inspect.isclass)
                hasfunction = inspect.getmembers(eval(moduleurl.__name__), inspect.isfunction)
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
                if ('__file__' in dir(eval(moduleurl.__name__))):
                    nodes.append({'name': moduleurl.__name__, 'file': eval(moduleurl.__name__).__file__,'layer':layer,'hasclass':classcount,'myclass':myclass,"hasfunction":functioncount,"myfunction":myfunction})
                else:
                    nodes.append({'name': moduleurl.__name__, 'file': 'null', 'layer': layer,
                                  'hasclass': classcount, 'myclass': myclass, "hasfunction": functioncount,
                                  "myfunction": myfunction})

                #             print()
                #             print('-----------')
                #             print(mname)
                get_modules(eval(moduleurl.__name__),filename,layer)
    return modules



def get_links(mymodule,str):
    for m in mymodule:
        nextmodules = []
        print(m)
        mm = inspect.getmembers(eval(m), inspect.ismodule)
        print(mm)
        print('--------------------------')
        for (name, moduleurl) in mm:
            if str in moduleurl.__name__:
                nextmodules.append(moduleurl.__name__)

        for n in nextmodules:
            links.append({'source': mymodule.index(m), 'target': mymodule.index(n)})

    print(links)
    return links



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

    mnetjson['nodes'] = nodes
    mnetjson['links'] = links

    print(mnetjson)
    print('----end----')

    f = open('../static/netjson/'+filename+'.json', 'w')
    f.write(json.dumps(mnetjson))
    f.close()

#path = r'C:\Python36\Lib\site-packages'
path = r'D:\ProgramData\Anaconda3\Lib\site-packages'
filename = 'torchvision'
# #
netjson(filename)
