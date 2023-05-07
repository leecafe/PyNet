#未完待续，2021年1月7日，有个Bug没搞定，对比文件pyNet4Inspect.py
import inspect
import json
import importlib
#pylibs=['alembic', 'aniso8601', 'argon2-cffi', 'attrs', 'Babel', 'backcall', 'baidu-aip', 'beautifulsoup4', 'bleach', 'bs4', 'certifi', 'cffi', 'chardet', 'chart-studio', 'chinesename', 'click', 'cloudpickle', 'colorama', 'cycler', 'dask', 'decorator', 'defusedxml', 'dlib', 'dominate', 'entrypoints', 'face-recognition', 'face-recognition-models', 'facenet-pytorch', 'ffmpeg-python', 'filetype', 'Flask', 'Flask-Admin', 'Flask-Babel', 'Flask-BabelEx', 'Flask-Bootstrap', 'Flask-Cache', 'Flask-Cors', 'Flask-Login', 'Flask-Migrate', 'Flask-RESTful', 'Flask-Script', 'Flask-SQLAlchemy', 'Flask-Testing', 'Flask-Uploads', 'Flask-WTF', 'future', 'HTMLParser', 'idna', 'importlib-metadata', 'inflect', 'ipykernel', 'ipython', 'ipython-genutils', 'ipywidgets', 'itsdangerous', 'jedi', 'jieba', 'Jinja2', 'joblib', 'jsonschema', 'jupyter', 'jupyter-client', 'jupyter-console', 'jupyter-core', 'kiwisolver', 'List', 'lxml', 'Mako', 'MarkupSafe', 'matplotlib', 'mistune', 'mysql-connector', 'mysqlclient', 'nbconvert', 'nbformat', 'neobolt', 'neotime', 'networkx', 'nltk', 'notebook', 'numpy', 'opencv-python', 'packaging', 'pandas', 'pandas-alive', 'pandocfilters', 'parso', 'pdfminer', 'peewee', 'pickleshare', 'Pillow', 'pip', 'plotly', 'pocketsphinx', 'prettytable', 'prometheus-client', 'prompt-toolkit', 'py2neo', 'pycparser', 'pycryptodome', 'pyecharts', 'Pygments', 'pymysql', 'pyparsing', 'pyrsistent', 'pytesseract', 'python-dateutil', 'python-editor', 'python-Levenshtein', 'pytz', 'PyWavelets', 'pywin32', 'pywinpty', 'PyYAML', 'pyzmq', 'qtconsole', 'QtPy', 'requests', 'retrying', 'scikit-image', 'scikit-learn', 'scipy', 'Send2Trash', 'setuptools', 'simplejson', 'six', 'sklearn', 'soupsieve', 'speaklater', 'sqlacodegen', 'SQLAlchemy', 'terminado', 'testpath', 'toolz', 'torch', 'torchvision', 'tornado', 'tqdm', 'traitlets', 'urllib3', 'visitor', 'Wand', 'wcwidth', 'webencodings', 'Werkzeug', 'wheel', 'widgetsnbextension', 'wordcloud', 'WTForms', 'xlrd', 'zipp']

pylibs=['bs4','wordcloud']

for p in pylibs:
    print(__import__(p))
    __import__(p)

def get_modules(toplib,arg,str):
    mylib = importlib.import_module(toplib)
    #print(mylib)
    mmembers = inspect.getmembers(arg, inspect.ismodule)
    #print(mmembers)
    #print('--------------------------')
    for (name, moduleurl) in mmembers:
        # print("name="+name)
        # print(moduleurl.__name__)
        if str in moduleurl.__name__ and not(moduleurl.__name__ in modules):
            modules.append(moduleurl.__name__)
            #print(modules)
            mname = arg.__name__ + "." + name
            #print(type(mname))
            if '__file__' in dir(getattr(arg, name)):
                #print(eval(mname).__file__)
                nodes.append({'name': moduleurl.__name__, 'file': getattr(arg, name).__file__})
                #             print()
                #             print('-----------')
                #             print(mname)
                get_modules(toplib,getattr(arg, name),filename)
    return modules



def get_links(toplib,mymodule,str):
    mylib = importlib.__import__(toplib)
    print(mymodule)
    for m in mymodule:
        nextmodules = []
        print(type(m))
        # firststr=m[0:m.rindex('.')]
        # substr=m[m.index('.')+1:]
        # print(firststr+"."+substr)
        # __import__(toplib)
        mm = inspect.getmembers(mylib, inspect.ismodule)
        print(mm)
        # print('--------------------------')
        for (name, moduleurl) in mm:
            if str in moduleurl.__name__:
                nextmodules.append(moduleurl.__name__)

        for n in nextmodules:
            links.append({'source': mymodule.index(m), 'target': mymodule.index(n)})

    print(links)
    return links



def netjson(filename):
    #递归搜索模块Module节点
    #mylib=importlib.import_module(filename)

    mylib =importlib.__import__(filename)
    # print(dir(mylib))
    toplib=filename
    mymodule = get_modules(toplib,mylib,filename)
    print("nodes---------------------------")
    print(mymodule)
    print()

    get_links(toplib,mymodule,filename)

    mnetjson['nodes'] = nodes
    mnetjson['links'] = links

    print(mnetjson)

    f = open('../static/netjson/'+filename+'.json', 'w')
    f.write(json.dumps(mnetjson))
    f.close()

path = r'C:\Python36\Lib\site-packages'
for p in pylibs:
    modules = []
    mnetjson = {'nodes': '', 'links': ''}
    nodes = []
    links = []
    filename = p
    netjson(filename)
