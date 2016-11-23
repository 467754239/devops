# Paxos VS Raft
> 分布式一致性算法

[raft英文](./raft/raft.pdf)

[raft中文](https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md)

---

> paxos

```
zookeeper 一致性算法是paxos


Paxos算法的目标就是让他们按照少数服从多数的方式，最终达成一致意见。


<!-- 意见领袖 提出 提议，接受者处理这个提议 yes -->no
    号大就是意见领袖 意见领袖就是提议者

```

> raft

```
etcd、consul、redis cluster 一致性算法是raft
```