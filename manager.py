from flask import Flask,render_template,request
import inspect
app=Flask(__name__)
@app.route('/head')
def head():
    return render_template('head.html')
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/tree')
def tree():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted + '.json'
        jfile=wanted
    else:
        jsonfile = "bs4.json"
        jfile="bs4"
    return render_template('filetree.htm', jsonfile=jsonfile,jfile=jfile)
    #return render_template('filetree.htm')

@app.route('/leetree')
def leetree():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted + '.json'
        jfile=wanted
    else:
        jsonfile = "bs4.json"
        jfile="bs4"
    return render_template('pytreeRandomSize2021.htm', jsonfile=jsonfile,jfile=jfile)  #pytreeRandomSize2021.htm
    #return render_template('filetree.htm')
@app.route('/hicircle')
def hicircle():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted + '.json'
        jfile=wanted
    else:
        jsonfile = 'flare.json'
        jfile = 'flare'
    return render_template('hiCircle.htm', jsonfile=jsonfile,jfile=jfile)

@app.route('/matrix')
def matrix():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted + '.json'
        jfile=wanted
    else:
        jsonfile="pylibs.json"
        jfile="pylibs"
    return render_template('matrix2021.html', jsonfile=jsonfile,jfile=jfile)

@app.route('/pylibs/<name>')
def info(name):
    if name:
        import os
        libinfo = os.popen(r'c:\python36\scripts\pip3 show ' + name).read()
        relist = []
        relist = libinfo.split('\n')
    return render_template('pylibs.html', libinfo=relist)

@app.route('/detail')
def detail():
    wanted= request.args.get("wanted", type=str)
    print(wanted)
    import numpy
    import open3d
    import networkx
    import wordcloud
    filename = inspect.getmembers(eval(wanted),inspect.ismodule)
    docs = inspect.getdoc(eval(wanted))
    dirinfo=dir(eval(wanted))
    return render_template('detail.html', filename=filename,docs=docs,dirinfo=dirinfo)

@app.route('/network')
def libs():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted+'.json'
        jfile=wanted
    else:
        jsonfile = "pylibs.json"
        jfile="pylibs"
    return render_template('pyclass.html', jsonfile=jsonfile,jfile=jfile)

@app.route('/bubble')
def bubble():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted+'.json'
        jfile=wanted
    else:
        jsonfile = 'flare-2.json'
        jfile = 'flare-2'
    return render_template('bubble.htm', jsonfile=jsonfile,jfile=jfile)

@app.route('/wordcloud')
def wc():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted+'.json'
        jfile=wanted
    else:
        jsonfile = "pylibs.json"
        jfile = "pylibs"
    return render_template('wordcloud.htm', jsonfile=jsonfile,jfile=jfile)

@app.route('/treenet')
def treenet():
    wanted = request.args.get("wanted", type=str)
    if wanted:
        jsonfile = wanted + '.json'
        jfile = wanted
    else:
        jsonfile = 'flare.json'
        jfile = 'flare'
    return render_template('treenet2021.htm', jsonfile=jsonfile, jfile=jfile)
if __name__=='__main__':
    app.run(port=5000)
