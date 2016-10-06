## nohup
```
nohup(n ohang up)
中文意思就是不挂起的意思

$ man nohup  //查看对应的帮助说明.
运行COMMAND，忽略挂起SIGHUP信号.
标准输出和标准错误缺省会被重定向到 nohup.out 文件中

终端关闭后会给此终端下的每一个进程发送SIGHUP信号，从而关闭其所有子进程;
而使用nohup运行的进程则会忽略这个SIGHUP信号，因此终端关闭后进程也不会退出。
```

## flask session
```
flask中的session默认是完全保留在客户端浏览器中的，
也就是说我往flask的session中写入数据，最终这些数据将会以json字符串的形式，
经过base64编码写入到用户浏览器的cookie里，也就是说无须依赖第三方数据库保存 session数据，
也无需依赖文件来保存，这一点倒是挺有意思

SecureCookieSession
```

### supervise
```
系统进程监控管理器
功能是监控一个指定的服务，当该服务进程消亡，则重新启动该进程。

# wget http://cr.yp.to/daemontools/daemontools-0.76.tar.gz 
# tar -zxf daemontools-0.76.tar.gz 
# cd admin/daemontools-0.76 
# package/install   //此处会有报错
# vim src/conf-cc
在第一行最后加上 -include /usr/include/errno.h

# wget http://smarden.org/pape/djb/manpages/daemontools-0.76-man.tar.gz 
# tar zxf daemontools-0.76-man.tar.gz 
# cd daemontools-man 
# gzip *.8 
# cp *.8.gz /usr/share/man/man8

man svscan
cat /etc/inittab
会发现原来daemontools是使用init的方式来保护自己的：
SV:123456:respawn:/command/svscanboot

使用
# cd /opt/sengled/agent
# vim main.py
import time
while True:
    time.sleelp(1)

# vim run
source /etc/profile
python main.py

这样就可以了.
```

![supervise]()