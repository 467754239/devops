## supervise 
```
1. 介绍
系统进程监控管理器
功能是监控一个指定的服务，当该服务进程消亡，则重新启动该进程。

2. 安装
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

3. 功能补充
man svscan
cat /etc/inittab
会发现原来daemontools是使用init的方式来保护自己的：
SV:123456:respawn:/command/svscanboot

4. 示例
# cd /opt/sengled/agent
# vim main.py
import time
while True:
    time.sleelp(1)

# vim run
source /etc/profile
python main.py

```