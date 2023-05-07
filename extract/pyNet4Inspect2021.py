import bs4
import inspect
import json
import importlib
import numpy
import flask
import wordcloud
import dlib
import networkx
import nltk
from nltk import metrics,translate
import PIL
import pandas
from matplotlib import pyplot
import matplotlib
import open3d
import torch



modules = []
mnetjson = {'nodes': '', 'links': ''}
nodes = []
links = []


def get_modules(arg, str):
    if arg.__name__ == filename:
        modules.append(arg.__name__)
        nodes.append({'name': arg.__name__, 'file': arg.__file__})
    mmembers = inspect.getmembers(arg, inspect.ismodule)
    print(modules)
    print(mmembers)
    print('--------------------------')
    for (name, moduleurl) in mmembers:
        print("name=" + name)
        print(moduleurl.__name__)
        if str in moduleurl.__name__ and not (moduleurl.__name__ in modules):  # 判断没有被扫描到的Module
            modules.append(moduleurl.__name__)
            mname = arg.__name__ + "." + name
            # modules.append(mname)
            print(modules)

            # print(mname)
            print('__file__' in dir(eval(moduleurl.__name__)))
            if '__file__' in dir(eval(moduleurl.__name__)):
                # print(eval(mname).__file__)
                nodes.append({'name': moduleurl.__name__, 'file': eval(moduleurl.__name__).__file__})
                #             print()
                #             print('-----------')
                #             print(mname)
                get_modules(eval(moduleurl.__name__), filename)
            else:
                if len(inspect.getmembers(arg, inspect.ismodule)) > 0:
                    nodes.append({'name': moduleurl.__name__, 'file': 'null'})
                    get_modules(eval(moduleurl.__name__), filename)

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

    mymodule = get_modules(eval(filename),filename)
    print(mymodule)
    print()

    get_links(mymodule,filename)

    mnetjson['nodes'] = nodes
    mnetjson['links'] = links

    print(mnetjson)
    print('----end----')
    f = open('../static/netjson/'+filename+'.json', 'w')
    f.write(json.dumps(mnetjson))
    f.close()

path = r'C:\Python36\Lib\site-packages'
filename = 'torch'
# #
netjson(filename)
