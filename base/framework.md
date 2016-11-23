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