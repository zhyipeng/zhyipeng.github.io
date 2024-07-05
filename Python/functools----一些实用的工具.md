> 项目里面频繁见到 functools.wraps 装饰器，就抽了些时间来研究一下 functools 里面的东西。

## lru_cache -- 函数缓存

```python
@lru_cache(maxsize=128, typed=False)
```

这是一个为方法提供缓存功能的装饰器，在多次调用方法输入相同参数时可以直接返回方法结果，当然首先需要保证方法本身是幂等的才有意义

maxsize 是缓存的最大数量限制，默认 128，当设置为 None 是将无上限，设置为 2 的幂时可以获得最佳性能

typed = True 时，将对入参做类型检查，不同类型的入参会视为不一样的入参，如 f(3) 和 f(3.0)

为了方便调试，被装饰的方法会带有一个 cache_info() 方法，调用此方法会返回一个命名元组，包括命中次数 hits，未命中次数 misses，maxsize 和 当前缓存大小 currsize。还会带有一个清理缓存的函数 cache_clear()

该装饰器是在内存里以字典来存储缓存的，因此在多线程/进程环境下不一定能达到理想的状态

> 我们项目内自己实现了一个类似功能的装饰器，不过是基于 redis 和过期时间（而不是最大数量）的存储机制，所以在多个进程、甚至不同项目间都可以复用缓存



## total_ordering -- 快速实现全比较类

```python
@total_ordering
class ClassA:
    pass
```

对于一些自定义的数据结构，我们可能需要对两个实例之间做比较，或者使之适用于 sorted、max 等方法。通常我们的做法是实现这个类的 `__eq__`、`__lt__`、`__gt__`等全套的比较方法。而 total_ordering 这个类装饰器可以简化这个步骤，只需要实现类的 `__eq__` 方法和 `__lt__`、`__le__`、`__gt__`、`__ge__` 这四个方法中的其中一个，装饰器可以根据这些方法间的内部逻辑，帮我们实现剩下的比较方法。

> 虽然这种方法很偷懒，但是通常情况下会比手动实现的方法性能要差一些，因为它可能会多出一两步逻辑比较比如"非"操作。



## partial -- 简化函数调用

```python
def add(x, y):
    return x + y

add1 = partial(add, y=1)
```

在上面的例子中，给定一个加法的函数 add，如果想要实现自增的效果，可以很简单地给 y 加个默认值 1。

如果在此基础上还想要实现自减呢？是不是每次都要传 y=-1？

或者这样：

```python
def add(x, y):
    return x + y

def add1(x):
    return add(x, 1)

def sub1(x):
    return add(x, -1)
```

partial 提供了一个更优雅的解决方案，原理其实和上面的写法一样，写死了某些参数的传递，不过看起来会简洁很多

```python
add1 = partial(add, y=1)
sub1 = partial(add, y=-1)
```

> partial 可用于所有的可调用对象



## partialmethod -- 适用于对象方法的 partial

partialmethod 和 partial 的作用基本相同，只不过 partialmethod 可以作用于类的对象方法，即默认第一个参数会传 self。

也可以作用于 staticmethod、classmethod、abstractmethod、partialmethod，默认第一个参数会传到相应的参数



## reduce -- 累计计算

```python
reduce(func, iterable, init=None)
```

这个方法通常用于做一些累计、迭代的计算，比如最简单的阶乘：

```python
def factorial(n):
    return reduce(lambda x, y: x*y, range(1, n+1))
```

func 接收一个方法，该方法需要有两个入参，iterable 接收一个可迭代对象

init 是初始化值，如果为 None 的时候，func 的初始参数就是 iterable 的前两个值，否则是 init 和 iterable 的第一个值

reduce 会重复执行 func，并将返回值与 iterable 的下一个值分别作为下一次调用 func 的第一、第二个参数，知道 iterable 迭代完成，返回最后的结果

> 这个方法在 python2 是内置方法



## singledispatch -- python 中的重载函数

singledispatch 是用来实现 c++、java 等静态语言中重载函数功能的装饰器

```python
@singledispatch
def func(arg):
    print('Origin func: %s', arg)
    
@func.register
def _(arg: int):
    print('Int func: %s', arg)

@func.register
def _(arg: str):
    print('Str func: %s', arg)

@func.register
def _(arg: list):
    print('List func')
```

使用 singledispatch 将函数变成一个泛函数之后，就可以根据不同入参类型调用不同的函数处理，可以省去一堆的 if-else 判断。

当找不到对应的子函数的时候将会调用原函数处理。

子函数的命名不重要，所以可以直接用 _ 命名。



## update_wrapper -- 保留函数原本属性

这是一个装饰器：

```python
def decorator(func):
    def wrapper(*args, **kw):
        ret = func(*args, **kw)
        return ret
    return wrapper
```

装饰器的定义是在不改变函数定义的前提下给函数增加功能。然而这样装饰出来的函数其实已经不是原来的函数了，而是 wrapper 了，因此它的一些内部属性，比如 `__name__`、`__doc__` 等也发生了变化，update_wrapper 就是用来更新装饰函数，使之保留函数原本熟悉的方法。

直接看源码：

```python
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__', '__annotations__')
WRAPPER_UPDATES = ('__dict__',)

def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    wrapper.__wrapped__ = wrapped
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper
```

此时上述装饰器可以修改成

```python
def decorator(func):
    def wrapper(*args, **kw):
        ret = func(*args, **kw)
        return ret
    return update_wrapper(wrapper, func)
```

这样被装饰函数 func 的 `__name__`、`__doc__` 等属性就会保持不变了



## wraps -- update_wrapper 的装饰器版本

```python
def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
```

很简单，就是 update_wrapper 的装饰器版本。

这样上述装饰器就可以写成这样：

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kw):
        ret = func(*args, **kw)
        return ret
    return wrapper
```