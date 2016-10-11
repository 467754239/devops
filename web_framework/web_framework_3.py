#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from wsgiref.simple_server import make_server

 
def RunServer(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    url = environ['PATH_INFO']
    if url == "/":
        return 'redirect /login/'
    elif url == '/login/':
        return 'login'
    elif url == '/logout/':
        return 'logout'
    else:
        return '404'
 
if __name__ == '__main__':
    httpd = make_server('', 8000, RunServer)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()
