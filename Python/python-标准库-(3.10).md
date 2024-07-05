> 一些标准库简要笔记


- heapq - 内置的堆结构和堆算法
- statistics - 数学统计函数, 均值, 方差等...
- itertools - 很多方便的迭代器, 如 cycle() ...
- fileinput - 需要读取多个文件时很好用
- tempfile - 生成临时文件
- glob, fnmatch - Unix 风格的路径通配符, 脚本可能会用到
- shelve - 基于单文件存储的 Key-Value 数据库? 内部使用 pickle 序列化对象, 以及 dbm 风格的数据库接口
- configparser - 配置文件解析器
- plistlib - .plist 文件解析器, 比如可配合 launchctl 实现一个 mac 下的定时任务管理器
- getpass - 命令行的密码输入工具
- sched - 事件调度器, 轻量级的定时任务调度器
- webbrowser - 调用默认浏览器搞事情
- 2to3 - 将 python2 代码转为 python3 代码
- contextvars - 上下文变量, 对标 flask 的 request 等变量, 原生支持 asyncio, 其他情况需要做一些额外配置才能使用.
