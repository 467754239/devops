#!/usr/bin/env python
#coding:utf-8

import socket

'''
GET /index.html HTTP/1.1
Host: 54.222.146.205:8000
'''

resp = '''HTTP/1.1 200 OK\r\nContent-Length: 15\r\n\r\n<h1>zhengyscn</h1>'''

HOST = ''
PORT = 8000 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
'''
backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
这个值不能无限大，因为要在内核中维护连接队列
'''
s.listen(5) #backlog

while True:
    conn, addr = s.accept()
    print 'Connected by', addr

    output = ''
    while '\r\n\r\n' not in output:
        recv_data = conn.recv(1)
        output += recv_data
    print 'url: ', output.split('\n')[0].split()[1]
    conn.sendall(resp)
    conn.close()

