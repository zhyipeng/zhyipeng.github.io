# python

### 内置 http 服务
```bash
python -m SimpleHTTPServer 7777
python3 -m http.server 7777
```

### 基于 redis 实现的并发锁
```python
@contextmanager
def redlock_manager(key, ttl=3, blocking_timeout=None):
    lock = redis_client.lock(key,
                             timeout=ttl,
                             blocking_timeout=blocking_timeout)
    locked = lock.acquire()

    try:
        yield locked
    finally:
        if locked:
            try:
                lock.release()
            except (LockError, LockNotOwnedError):
                pass
```

### 短 uuid
```python
def uuid4_hex(duplicate=1):
    s = ''
    for _ in range(duplicate):
        s += uuid.uuid4().hex
    return s


def short_uuid():
    uuid = uuid4_hex()
    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    s = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        s += chars[x % 0x3E]
    return s
```

### 自动重试机制
```python
class ExecRetry(Exception):
    pass


class with_retry:
    """
    :param retry_times: max retry times
    :param result: return value when exec over max retry times
    exec_retry: raise this parameter to exec retry
    """
    exec_retry = ExecRetry

    def __init__(self, retry_times: int = 5, result: typing.Any = None):
        self.max_retry_times = retry_times
        self.result = result
        self.exec_times = 0

    def return_default_result(self) -> typing.Any:
        if isinstance(self.result, Exception):
            raise self.result
        else:
            return self.result

    def __call__(self, func: typing.Callable) -> typing.Callable:

        def wrapped(*args, **kwargs) -> typing.Any:
            if self.exec_times > self.max_retry_times:
                return self.return_default_result()
            try:
                return func(*args, **kwargs)
            except ExecRetry:
                self.exec_times += 1
                return wrapped(*args, **kwargs)

        functools.update_wrapper(wrapped, func)
        return wrapped
```

### 二分查找
```python
import bisect


# BREAKPOINTS 必须是已经排好序的，不然无法进行二分查找
BREAKPOINTS = (1, 60, 3600, 3600 * 24)
TMPLS = (
    # unit, template
    (1, "less than 1 second ago"),
    (1, "{units} seconds ago"),
    (60, "{units} minutes ago"),
    (3600, "{units} hours ago"),
    (3600 * 24, "{units} days ago"),
)


def from_now(ts):
    """接收一个过去的时间戳，返回距离当前时间的相对时间文字描述
    """
    seconds_delta = int(time.time() - ts)
    unit, tmpl = TMPLS[bisect.bisect(BREAKPOINTS, seconds_delta)]
    return tmpl.format(units=seconds_delta // unit)
```

### wrapt库
```python
import wrapt

def provide_number(min_num, max_num):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # 参数含义：
        #
        # - wrapped：被装饰的函数或类方法
        # - instance：
        #   - 如果被装饰者为普通类方法，该值为类实例
        #   - 如果被装饰者为 classmethod 类方法，该值为类
        #   - 如果被装饰者为类/函数/静态方法，该值为 None
        #
        # - args：调用时的位置参数（注意没有 * 符号）
        # - kwargs：调用时的关键字参数（注意没有 ** 符号）
        #
        num = random.randint(min_num, max_num)
        # 无需关注 wrapped 是类方法或普通函数，直接在头部追加参数
        args = (num,) + args
        return wrapped(*args, **kwargs)
    return wrapper
```

### FastAPI 处理 XML-body 数据
```python
from xml.etree.ElementTree import fromstring
from fastapi import Depends, Request

# FastAPI Depends
async def parse_xml_data(request: Request) -> dict[str, Any]:
    body = await request.body()
		xml_tree = fromstring(body)
		return {node.tag: node.text for node in xml_tree}


@app.post('/')
async def api(data: dict[str, Any] = Depends(parse_xml_data)):
		return data
```