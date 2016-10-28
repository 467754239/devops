## nohup
```
nohup(n ohang up)
中文意思就是不挂起的意思

# 语法
$ nohup command > out.log 2&1 &

当进程不是守护进程时，不能简单地在命令行后添加一个&，当终端关闭时，该进程也随之关闭。因为通常在终端起动的进程其父进程是终端进程,
也就是大家常说的init进程，当终端关闭时，其所有子进程也随之关闭。

nohup的作用终端关闭后会给此终端下的每一个进程发送SIGHUP信号，从而关闭其所有子进程;而使用nohup运行的进程则会忽略这个SIGHUP信号，
因此终端关闭后进程也不会退出。

使用2>&1将标准错误输出也重定向到标准输出中，因为预定义的STDIN，STDOUT，STDERR分别是0，1，2。
```

## flask session
```
flask中的session默认是完全保留在客户端浏览器中的，
也就是说我往flask的session中写入数据，最终这些数据将会以json字符串的形式，
经过base64编码写入到用户浏览器的cookie里，也就是说无须依赖第三方数据库保存 session数据，
也无需依赖文件来保存，这一点倒是挺有意思

SecureCookieSession
```

## WSGI
```
WSGI是Web Server Gateway Interface的缩写
Python内置了一个WSGI服务器，这个模块叫wsgiref，它是用纯Python编写的WSGI服务器的参考实现。

## 参考文章
http://www.kancloud.cn/wizardforcel/liaoxuefeng/108705
http://archimedeanco.com/wsgi-tutorial/
http://wsgi.readthedocs.io/en/latest/
```

## 阐述Python Web框架(framework)
[自定义Web框架](https://github.com/467754239/devops/tree/master/web_framework)
```
## Python Web开源框架
flask、django、tornado、web.py

## 框架的组成
socket、url、view、model......

## Python Web框架分为两类
(1) 第一类
wsgi + web framework
这一类的框架代表有flask、django
不负责处理底层socket通信以及HTTP请求解析等，只处理更高层次的逻辑处理.

(2) 第二类
web framework
这一类的框架代表有tornado

tornado = socket + web framework
django/flask = wsgi + web framework

注意：tornado既可以实现用wsgi也可以写原生的socket等.

## jiaja2引擎
# pip install jinja2

>>> from jinja2 import Template
>>> template = Template('Hello {{ name }}!')
>>> template.render(name='John Doe') == u'Hello John Doe!'
True

## MVC 与 MTV工作模型
(1) MVC模型
Models Views Controllers
Models：        存放数据库操作.
Views:          存放html文件.
Controllers:    存放处理函数.

(2) MTV模型
Models Templates Views
Models：        存放数据库操作.
Templates:      存放html文件.
Views:          存放处理函数.

## Jinja2文档
http://docs.jinkan.org/docs/jinja2/
```

## subprocess.Popen
```
参考文章
http://zhoutall.com/archives/469
https://docs.python.org/2/library/subprocess.html
http://denizeren.net/2014/07/14/flask-file-descriptor-inheritance-problem/

## 程序结构描述
主线程为Flask，默认监听在5000端口上，其它功能用子线程来执行；
子线程中有调用subprocess模块启动指定的服务(比如nginx、java等);

## 问题
主线程退出，子线程占用主线程的5000端口.
和下面这个链接遇到问题很类似
http://denizeren.net/2014/07/14/flask-file-descriptor-inheritance-problem/

>>> subprocess.Popen?
If close_fds is true, all file descriptors except 0, 1 and 2 will be closed before the child process is executed. (Unix only). Or, on Windows, if close_fds is true then no handles will be inherited by the child process. Note that on Windows, you cannot set close_fds to true and also redirect the standard handles by setting stdin, stdout or stderr.
译
如果参数close_fds是True，所有的文件描述符除了0, 1 and 2都将要被关闭在子进程被执行之前，在(Unix only)；
或者在Windows如果close_fds是True那么没有被处理的都将被子进程继承.
注意：在Windows上你不能设置close_fds 为True并且不能重定向stdin, stdout or stderr.
```

## 文件描述符
```
文件描述符是操作系统为每个进程维护的一个结构体数组的索引（下标）。因此fd一定是非负整数。
内核会为进程打开的每个文件分配一个结构体来存放文件的相关信息，这个结构体在结构体数组中的下标即为该文件的文件描述符。
系统打开文件后创建的一种标签，描述了这个打开文件目录的一些状态.
一个结构体，其中的数据项纪录了文件的路径，状态，当前写的位置.
os.dup2(old_fd, new_fd)函数的作用是将下标为old_fd的结构体复制到new_fd对应的结构体，从而使两个结构体得内容相同。
```

## ansible sourceCode
Ansible部分源代码[查看](./ansible_sourcecode)

## signal(SIGCHLD, SIG_IGN)和signal(SIGPIPE, SIG_IGN)
```
原文出自: http://blog.chinaunix.net/uid-20775448-id-3492910.html

signal(SIGCHLD, SIG_IGN);
因为并发服务器常常fork很多子进程，子进程终结之后需要服务器进程去wait清理资源。如果将此信号的处理方式设为忽略，可让内核把僵尸子进程转交给init进程去处理，省去了大量僵尸进程占用系统资源。(Linux Only)
对于某些进程，特别是服务器进程往往在请求到来时生成子进程处理请求。如果父进程不等待子进程结束，子进程将成为僵尸进程（zombie）从而占用系统资源。如果父进程等待子进程结束，将增加父进程的负担，影响服务器进程的并发性能。在Linux下可以简单地将 SIGCHLD信号的操作设为SIG_IGN。
 
signal(SIGPIPE, SIG_IGN);
TCP是全双工的信道, 可以看作两条单工信道, TCP连接两端的两个端点各负责一条. 当对端调用close时, 虽然本意是关闭整个两条信道, 
但本端只是收到FIN包. 按照TCP协议的语义, 表示对端只是关闭了其所负责的那一条单工信道, 仍然可以继续接收数据. 也就是说, 因为TCP协议的限制, 
一个端点无法获知对端的socket是调用了close还是shutdown.
对一个已经收到FIN包的socket调用read方法, 
如果接收缓冲已空, 则返回0, 这就是常说的表示连接关闭. 但第一次对其调用write方法时, 如果发送缓冲没问题, 会返回正确写入(发送). 
但发送的报文会导致对端发送RST报文, 因为对端的socket已经调用了close, 完全关闭, 既不发送, 也不接收数据. 所以, 
第二次调用write方法(假设在收到RST之后), 会生成SIGPIPE信号, 导致进程退出.
为了避免进程退出, 可以捕获SIGPIPE信号, 或者忽略它, 给它设置SIG_IGN信号处理函数:
signal(SIGPIPE, SIG_IGN);
这样, 第二次调用write方法时, 会返回-1, 同时errno置为SIGPIPE. 程序便能知道对端已经关闭.
```

## 简易版httpserver
> 单进程 | 多进程 | 多线程 | 线程池

(点击链接)[./simple_server]

## 异步I/O select
```
select
```

## 学习Blog
```
# Stack Overflow
http://stackoverflow.com/

# flask、django
http://blog.igevin.info/archive/

<flask response>
http://www.programcreek.com/python/example/51515/flask.Response

# Python
http://www.kancloud.cn/wizardforcel/liaoxuefeng/108427

<python Example搜索 挺好的>
http://www.programcreek.com/python/

# Git
https://github.com/flyhigher139/Git-Cheat-Sheet

# sumline
https://github.com/jikeytang/sublime-text
```

## 源码分析
```
# httpbin
https://github.com/Runscope/httpbin
# flask
https://github.com/pallets/flask
# ansible
https://github.com/ansible/ansible
```
