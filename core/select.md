## 异步I/O select

```
select

传统的socket在处理并发方面有所欠缺，借助select模块能够较好的要非阻塞IO

处理异步IO
能够监视文件描述符的变化

select的一个缺点在于单个进程能够监视的文件描述符的数量存在最大限制。

select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)
以列表形式接收四个参数
rlist   可读文件对象，输入.
wlist   可写文件对象，输出.
xlist   异常文件对象，异常.
timeout 超时设置，可选.单位秒，表示多长时间监听一次.

当监控的对象发生变化时，select会返回发生变化的对象列表.

ansible中也是用了select监听事件的方式.
```