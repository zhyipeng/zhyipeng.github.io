> 实现 "等待网络输入"

假设有个需求, 在终端接受用户输入并打印出来, 这是个初学者常见的需求:

```python
def foo():
    print('waiting input')
    ret = input('please input: ')
    print(ret)
```

很简单, 那么现在需求升级, 我希望接收来自于网络用户的输入, 比如通过 http/rpc 调用的输入, 怎么做呢?

这个过程包括:
1. 服务器执行前序代码, 即 `print('waiting input')`
2. 通知客户端服务端已经准备好接收输入, 即上述例子中的 `input`方法
3. 等待输入
4. 接收到输入然后进行后续处理 `print(ret)`

通常我们会在网络请求消息体中增加一个类似协议号的东西来区分不同场景下的输入输出(http的话可能是 restful api):
```python
def foo():
    print('waiting input')
    send_to_client(cmd=1)


def handler(cmd, data):
    """处理客户端请求"""
    if cmd == 2:
        ret = data
        print(ret)
```

这种处理方式很常见, 也能够很好的完成工作. 但是会导致代码连贯性变差, `foo` 的逻辑被拆成了两部分.

参考 `async/await` 可以使异步代码看起来像同步代码, 我们可以尝试将 `foo` 方法改造成这样:

```python
async def foo():
    print('waiting input')
    ret = await ainput('please input: ')
    print(ret)
```

只要实现 `ainput` 方法内部等待网络 io 的逻辑即可, 等待一个信号或者资源可以使用 `asyncio.Event/asyncio.Queue` 来实现

```python
queue = asyncio.Queue()

async def ainput():
    await send_to_clent(cmd=1)
    return await queue.get()


async def handler(cmd, data):
    """处理客户端请求"""
    if cmd == 2:
        await queue.put(data)
```

这样可以保证业务逻辑的连贯性. handler 内部只需要做好消息分发, 而不需要考虑业务逻辑.
