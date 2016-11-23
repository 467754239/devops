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