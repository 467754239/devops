## 知乎文章
```
## 如何优雅地使用 Stack Overflow？
https://www.zhihu.com/question/20824615

## 为什么 Flask 有那么多的好评?
https://www.zhihu.com/question/28902969

## 怎样才能彻底掌握flask？怎么个学习顺序比较合理？
https://www.zhihu.com/question/20135205

## 有哪些python+flask的搭建的博客或论坛开源推荐？
https://www.zhihu.com/question/40746923
```

## 源码分析
```
# flask
https://github.com/pallets/flask

# httpbin
https://github.com/Runscope/httpbin
```

## nohup
```
nohup(n ohang up)
中文意思就是不挂起的意思

当进程不是守护进程时，不能简单地在命令行后添加一个&，当终端关闭时，该进程也随之关闭。因为通常在终端起动的进程其父进程是终端进程,
也就是大家常说的init进程，当终端关闭时，其所有子进程也随之关闭。

## 语法
$ nohup command > out.log 2&1 &
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

## Python subprocess.Popen
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
```
