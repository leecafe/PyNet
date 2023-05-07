#!/usr/bin/env python
# coding: utf-8

# In[23]:


import inspect
import nltk

modules = []
mnetjson = {'nodes': '', 'links': ''}
nodes = []
links = []


def get_modules(arg, str):
    #print(arg.__name__, str)
    if arg.__name__ == filename:
        modules.append(arg.__name__)
        nodes.append({'name': arg.__name__, 'file': arg.__file__})
    if(len(modules)>1):
        modules.pop()
        nodes.pop()
    mmembers = inspect.getmembers(arg, inspect.ismodule)
    # print(modules)
    # print(nodes)
    # print(mmembers[0:3])
    # print('--------------------------')
    for (name, moduleurl) in mmembers:
#         print("name=" + name)
#         print(moduleurl.__name__)
#         print("===============")
        if str in moduleurl.__name__ and not (moduleurl.__name__ in modules):  # 判断没有被扫描到的Module
            modules.append(moduleurl.__name__)
            #print(modules)
            
            # print(moduleurl.__name__)
            # print('__file__' in dir(moduleurl))
            if '__file__' in dir(moduleurl):
                nodes.append({'name': moduleurl.__name__, 'file': moduleurl.__file__})
                # print(nodes)
                # print("------------3--------------")
                
                #get_modules(eval(moduleurl.__name__), filename)
                #__import__(moduleurl.__name__)
                #print(moduleurl.__name__, filename)
                #print(__import__(moduleurl.__name__))
                get_modules(__import__(moduleurl.__name__), filename)
            else:
                # print("----------4-------------")
                if len(inspect.getmembers(arg, inspect.ismodule)) > 0:
                    nodes.append({'name': moduleurl.__name__, 'file': 'null'})
                    get_modules(__import__(moduleurl.__name__), filename)

    return modules, nodes


filename = 'nltk'
get_modules(eval(filename), filename)


# In[ ]:




