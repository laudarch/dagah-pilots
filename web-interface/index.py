from bottle import route, run, template, static_file
import subprocess

@route('/index.js')
def index_js():
    return static_file('index.js', root='./')

@route('/index.css')
def index_js():
    return static_file('index.css', root='./')

@route('/index.html')
def index_html():
    output = template('index')
    return output

@route('/ls')
def ls():
    p = subprocess.Popen("ls -lah", stdout=subprocess.PIPE, shell=True)
    output = template('ls',process=p)
    return output

@route('/ps')
def ps():
    p = subprocess.Popen("ps -ef", stdout=subprocess.PIPE, shell=True)
    output = template('ls',process=p)
    return output

run(host='192.168.203.128')
