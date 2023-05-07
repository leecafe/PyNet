import bs4
import wordcloud
import inspect
import json

classes = []
cnetjson = {'nodes': '', 'links': ''}
nodes = []
links = []


def get_classes(arg,str):
    if arg.__name__ == filename:
        classes.append(arg.__name__)
        nodes.append({'name': arg.__name__, 'classpath': arg.__package__+"."+arg.__name__})
        print(nodes)
    cmembers = inspect.getmembers(arg, inspect.isclass)
    print(cmembers)
    for (name, classurl) in cmembers:
        classname=classurl.__module__+"."+classurl.__name__
        print(classname)
        if str in classname and not(classname in classes):
            print(str+"--1--")
            print(classname + "-------2-------")
            print(classes)
            classes.append(classname)
            nodes.append({'name': classname, 'classpath': classname})
            print("module-name="+classurl.__module__)
            get_classes(eval(classurl.__module__),filename)
    return classes



def get_clinks(myclass,str):
    for m in myclass:
        print(m)
        nextclasses = []

        if m==str:
            mm = inspect.getmembers(eval(m), inspect.isclass)
        else:
            print(eval(m).__module__)
            mm = inspect.getmembers(eval(eval(m).__module__), inspect.isclass)
        print(mm)
        for (name, classurl) in mm:
            classname = classurl.__module__ + "." + classurl.__name__
            if str in classname and not(classname == m):   #有错误，上级模块可能相同
                nextclasses.append(classname)

        print(nextclasses)
        for n in nextclasses:
            links.append({'source': myclass.index(m), 'target': myclass.index(n)})

    print(links)
    return links



def classnetjson(filename):
    #递归搜索模块Module节点

    myclass = get_classes(eval(filename),filename)
    print(myclass)
    print(len(myclass))
    print()

    get_clinks(myclass,filename)

    cnetjson['nodes'] = nodes
    cnetjson['links'] = links

    f = open('../static/classnetjson/'+filename+'.json', 'w')
    f.write(json.dumps(cnetjson))
    f.close()

path = r'C:\Python36\Lib\site-packages'
filename = 'wordcloud'
# #
classnetjson(filename)
