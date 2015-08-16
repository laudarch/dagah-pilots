from bottle import route, run, template, static_file
import subprocess

@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='./images', mimetype='image/png')

@route('/index.js')
def index_js():
    return static_file('index.js', root='./')

@route('/jquery-ui.min.css')
def jquery_css():
    return static_file('jquery-ui.min.css', root='./')

@route('/jquery.js')
def jquery_css():
    return static_file('jquery.js', root='./')

@route('/jquery-ui.min.js')
def jquery_css():
    return static_file('jquery-ui.min.js', root='./')

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
