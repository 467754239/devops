#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from wsgiref.simple_server import make_server

def index():
    return '<h1>index</h1>'

def login():
    return '<h1>login</h1>'

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
