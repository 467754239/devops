#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from wsgiref.simple_server import make_server
from jinja2 import Template

def index():
    data = open('index2.html', 'r').read()
    template = Template(data)
    response = template.render(title='BookManage', books=['Python', 'Golang', 'jQuery'])
    return response.encode('utf-8') 

def login():
    f = open('login.html', 'r')
    data = f.read()
    return data 

def logout():
    return '<h1>logout</h1>'

url_for = {
    ('/', index),
    ('/login/', login),
    ('/logout/', logout),
}

 
def RunServer(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    url = environ['PATH_INFO']
    for define_url in url_for:
        if define_url[0] == url:
            return define_url[1]()
    return '404'
 
if __name__ == '__main__':
    httpd = make_server('', 8000, RunServer)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()
