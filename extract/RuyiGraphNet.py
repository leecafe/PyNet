import re, os
import json

class RuyiGraphNet:
    def __init__(self):
        print("Hello GraphNet")

    def readFile(self,path):
        while True:
            #path =  input('Please enter the route of your project:').strip()
            if os.path.isdir(path) == True:
                break;
            else:
                print('Your directory is invalid.')
        return path

    def getNode(self, path, graph, pre=''):
        filelist = os.listdir(path)
        print(filelist)
        try:
            for tmp in filelist:
                pathTmp = os.path.join(path,tmp)
                if os.path.isdir(pathTmp) == True:
                    self.getNode(pathTmp, graph, pre + tmp + '.')
                elif pathTmp[pathTmp.rfind('.') + 1 :] == 'py':
                    node = pre + tmp
                    graph[node[:node.rfind('.')]]={ 'path': pathTmp , 'edge': { }}
        except PermissionError:
            pass
        #print(graph)

    def getEdge(self,graph):
        for key, values in graph.items():
            path = values['path']
            file = open(path, 'r', encoding='UTF-8')
            for line in file:
                tmp = re.match('import (.+)', line)
                if tmp:
                    nodes = tmp.group(1).split(',')
                    for node in nodes:
                        if node in graph.keys():
                            graph[key]['edge'][node] = 1
                tmp = re.match('from (.+) import (.+)', line)
                if tmp:
                    node = key
                    pack = tmp.group(1)
                    pys = tmp.group(2).split(',')
                    for py in pys:
                        py = py.strip()
                        for i in pack:
                            if i == '.':
                                node=node[:node.rfind('.')]
                            else:
                                break
                        if pack[0]=='.':
                            node = node + '.'+pack[pack.rfind('.')+1:]
                            if node[-1]!='.':
                                node = node + '.'
                            node = node + py
                        else:
                            node=pack+'.'+py
                        if node in graph.keys():
                            graph[key]['edge'][node] = 1
                        else:
                            node=node[:node.rfind('.')]
                            if node in graph.keys():
                                graph[key]['edge'][node] = 1
                            else:
                                node=node+'.__init__'
                                if node in graph.keys():
                                    graph[key]['edge'][node] = 1

    def printPajek(self,graph, pajekOut):
        file = open(pajekOut, 'w')
        print('''*Vertices %d''' % len(graph), file=file)
        vertices = {}
        cnt=0
        for key, values in graph.items():
            cnt += 1
            graph[key]['id'] = cnt
            vertices[key] = cnt
            print('''%d "%s"''' % (cnt,key), file=file)
        print('''*Arcs :1 "SAMPLK1"''', file=file)
        for key, values in graph.items():
            for kk,vv in values['edge'].items():
                print('''%d %d %d''' % (vertices[key], vertices[kk], vv), file=file)
        file.close()

    def printJson(self,jsonOut, pajekOut):
        f = open(pajekOut, 'r')
        lines = f.readlines()
        flag = 0
        netjson={"nodes": "", "links": ""}
        nodes = []
        edges = []
        for line in lines:
            if line[0] == '*':
                flag += 1
            elif flag == 1:
                tmp = re.search(r'"(.+)"', line)
                if tmp:
                    node = tmp.group(1)
                    nodes.append(node)
            elif flag == 2:
                tmp = line.split()
                edge = (int(tmp[0]) - 1, int(tmp[1]) - 1)
                edges.append(edge)
        f.close()
        pacs = {}
        dic = {}
        type = 1
        for node in nodes:
            tmp = node.split('.')
            if len(tmp) == 1:
                pac = tmp[0]
            else:
                pac = tmp[-2]
            if pac not in pacs.keys():
                pacs[pac] = type
                type += 1
            dic[node] = pacs[pac]
        num = []
        for node in nodes:
            num.append(0)
        for edge in edges:
            num[edge[0]] += 1
            num[edge[1]] += 1
        print(nodes)
        print(edges)

        nodesjson=[]
        linksjson=[]
        cnt = 0
        for node in nodes:
            nodesjson.append({"name" : node , "type" : dic[node] , "num" : num[cnt]})
            cnt += 1

        for edge in edges:
            linksjson.append({"source": edge[0], "target": edge[1]})

        netjson['nodes']=nodesjson
        netjson['links']=linksjson

        f = open(jsonOut, 'w')
        f.write(json.dumps(netjson))
        f.close()



if __name__ == '__main__':
    print(os.chdir('../static'))
#    path = os.path('E:\PythonViz\static\mysql')
#    if not path.exists():
    path = r'C:\Python36\Lib\site-packages'
    libname = "nltk"
    path = path + '\\' + libname
    pajekOut = r'pajek/'+libname+'.net'
    jsonOut = r'netjson/'+libname+'.json'
    package = []
    graph = {}
    mygraph=RuyiGraphNet()
    path = mygraph.readFile(path)
    mygraph.getNode(path, graph)
    mygraph.getEdge(graph)
    mygraph.printPajek(graph, pajekOut)
    mygraph.printJson(jsonOut, pajekOut)
    print(graph)