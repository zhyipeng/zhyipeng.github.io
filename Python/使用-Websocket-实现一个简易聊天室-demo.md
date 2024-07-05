> 主要是双向通信...

# 使用 Websocket 实现一个简易聊天室 demo

主要是双向通信...

依赖:
```bash
pip install websockets
```

服务端:

```python
import asyncio

import websockets
from websockets.legacy.server import WebSocketServerProtocol

# 保存客户端链接, 以备广播/主动推送使用
players: set[WebSocketServerProtocol] = set()


async def serve(ws: WebSocketServerProtocol):
    players.add(ws)
    # websockets 自带广播方法, 内部检查链接状态, 但是是同步的, 可以考虑放线程异步执行, 或者手动遍历, boardcast 方法内部也就是一个简单的遍历
    websockets.broadcast(players, f'system: {hash(ws)} joined')
    # 之所以不使用 async for 是因为没找到合适的时机处理 ConnectionClosedOK,
    # WebSocketServerProtocol.__aiter__ 会直接忽略掉, 不利于链接的状态维护(比如需要实时获取在线人数什么的)
    # 当然有些情况下可能更推荐继承 WebSocketServerProtocol 重写部分实现的形式
    while 1:
        try:
            msg = await ws.recv()
            websockets.broadcast(players, f'{hash(ws)}: {msg}')
        except websockets.ConnectionClosedOK:
            players.remove(ws)
            websockets.broadcast(players, f'system: {hash(ws)} leaved.')
            break


async def main():
    async with websockets.serve(serve, "", 8765):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())

```

客户端:
懒得实现客户端了, 直接用 websockets-cli 代替吧:

开多几个 cli 试一下就行
```bash
python -m websockets ws://localhost:8765
```
