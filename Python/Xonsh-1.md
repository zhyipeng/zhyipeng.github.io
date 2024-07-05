> Xonsh 是一款支持 Python 语法的 shell

python作为一款优秀的脚本语言, 在很多情况下已经可以和bash脚本打架了, 尤其是对于开发来说.

在我日常使用终端的时候, 也常常会打开一个 ipython shell 来进行一些文本操作, 数值计算等. 值得一提的是 ipython 本身可以支持少数常用的 bash 命令, 如 ls, pwd... 其实本质上还是封装的 python 函数而已. 

<br/>

如果能真正把 python 和 bash 糅合到一起, 就很美妙了. 然后, 我发现了个神器 -- xonsh shell

<br/>

xonsh 不仅仅做到了同时支持 python 和 bash 语法, 还支持混着使用:

```bash
>>> pwd
/Users/zhyipeng
>>> app = 'python'
>>> cd @(os.path.dirname($(which @(app))))
>>> pwd
/usr/bin
```

>  一条简单的命令: 进入某个可执行文件所在的目录

<br/>

有一些命令是同时满足 bash 和 python 语法的, 这种场景下 xonsh 如何去解析呢?

```bash
>>> ls  # ls 命令
tmp
>>> ls = 5  # 声明一个变量名为 ls 并赋值
>>> ls  # 此时 ls 已在 python 上下文中, 因此会输出值
5
>>> ls -l  # 尝试解析为 python 语法失败, l 变量未声明, 继续尝试解析为 bash 语法
drwxr-xr-x  39 root  root        1248  6 11 09:59 tmp
>>> l = 4
>>> ls -l  # 成功解析为 python 语法
1
>>> del ls  # 释放 ls 变量
>>> ls
tmp

```

xonsh 拥有 python-mode 和 subprocess-mode(bash) 两种模式

- xonsh 优先尝试 python-mode
- 解析失败 (语法错误, 找不到变量等) 时继续尝试 subprocess-mode
- 若仍解析失败, 则保留为 python-mode
- 抛出异常

> Python模式和子进程模式之间的确定总是以尽可能安全的方式进行的。如果出现任何错误，它将倾向于python模式。两种模式之间的确定要在任何执行之前完成。您不需要担心部分执行的命令——这是不可能的。

<br/>

## 模式语法

**$()**

`$()` 语法用于指定 subprogress-mode 执行命令并捕获执行结果, 将标准输出作为 python 字符串返回:

```bash
>>> $(ls -l)
'total 0\n-rw-rw-r-- 1 snail snail 0 Mar  8 15:46 xonsh\n'
```

<br/>

**!()**

`!()` 语法和 `$()` 类似, 但是会返回更多的信息 -- 一个 CommandPipeline 对象

```bash
>>> !(ls -l)
CommandPipeline(
  stdin=<_io.BytesIO object at 0x10b40fa90>,
  stdout=<_io.BytesIO object at 0x10b60ddb0>,
  stderr=<_io.BytesIO object at 0x10b60dbd0>,
  pid=10892,
  returncode=0,
  args=['ls', '-l'],
  alias=['ls', '-G'],
  stdin_redirect=['<stdin>', 'r'],
  stdout_redirect=[7, 'wb'],
  stderr_redirect=[9, 'w'],
  timestamps=[1623394819.389607, 1623394819.401289],
  executed_cmd=['ls', '-G', '-l'],
  input='',
  output='total 0\n-rw-rw-r-- 1 snail snail 0 Mar  8 15:46 xonsh\n',
  errors=None
)
```

`CommandPipeline` 对象的 `__bool__` 方法的返回值取决于命令的返回码, 返回码为 0 时则返回 True.

<br/>

对 `CommandPipeline` 对象进行迭代就是对标准输出进行按行迭代, 这在处理一些命令的输出时会很有用 (典型的 `ls -l`)

<br/>

**$[]**

`$[]` 同 `$()` , 但是不会捕获标准输出, 其返回值始终是 None

```bash
>>> ret = $[ls -l]
total 0
-rw-rw-r-- 1 snail snail 0 Mar  8 15:46 xonsh
>>> ret is None
True
```

<br/>

**![]**

`![]` 也类似地对应 `!()` , 只是其返回值是 `HiddenCommandPipeline` 对象

```bash
>>> ret = ![ls -l]
total 0
-rw-rw-r-- 1 snail snail 0 Mar  8 15:46 xonsh
>>> ret

>>> type(ret)
xonsh.procs.pipelines.HiddenCommandPipeline
>>> ret.returncode
0
>>> ret.output
'total 0\n-rw-rw-r-- 1 snail snail 0 Mar  8 15:46 xonsh\n'
```

<br/>

**@()**

上述几个表达式通常是用来将 subprocess-mode 的返回值嵌入到 python-mode 中, 而 `@()` 表达式则反之, 一般用于将 python-mode 处理结果传递给 subprocess-mode:

```bash
>>> x = 'hello'
>>> y = 'xonsh'
>>> echo @(x + ' ' + y)
hello xonsh
>>> echo @(1 + 1)
3
>>> echo @([1, 'a'])
1 a
```

特别的, 当 `@()` 表达式用于 subprocess 的参数中, 并且其返回值是一个非 string 的可迭代对象时, 将会和起到类似 bash 中大括号拓展的效果:

```bash
>>> echo hello@(['world', 'xonsh'])
helloworld helloxonsh
>>> echo @(['a', 'b']):@(['x', 'y'])
a:x a:y b:x b:y
```

<br/>

**@$()**

用于特定场景: 将命令的输出代替命令本身, 如:

```bash
>>> # this returns a string representing stdout
>>> $(which ls)
'ls --color=auto\n'

>>> # this attempts to run the command, but as one argument
>>> # (looks for 'ls --color=auto\n' with spaces and newline)
>>> @($(which ls).strip())
xonsh: subprocess mode: command not found: ls --color=auto

>>> # this actually executes the intended command
>>> @([i.strip() for i in $(which ls).split()])
some_file  some_other_file

>>> # xonsh 提供了这种场景的缩写语法
>>> @$(which ls)
some_file  some_other_file
```

> 该例子是抄的官方文档的, 除了此场景我还没想到有其他类似的场景...

<br/>

## 管道

在 subprocess-mode 下, `|` 作为管道运算符可以正常工作, 而在 python-mode 下, `|` 则是 python 中的位运算符

<br/>

但是, 联想到管道的含义, 很容易有一个需求: 是否能把 subprocess 的返回值通过管道传递给 python 函数?

官方文档没有说明, 仅仅是在介绍 `@()` 表达式时提了一嘴. 经过一些简单实验, 得出结论:

可, 但是没那么简单.

```bash
>>> def foo(a, b):
        print(f'{a=}')
        print(f'{b=}')
        print(b.read())
        
>>> echo python | @(foo)
a=[]
b=<_io.TextIOWrapper name=3 encoding='utf-8'>
python

```

<br/>

简单地说是需要将一个函数用 `@()` 语法包裹作为管道的接收端, 该方法需要两个参数, 参数1 作用未知, 参数2 为 TextIOWrapper 对象, 可以调用 read() 方法获得管道传输的值, 当然还可以有更多参数, 也是 TextIOWrapper 对象, 只是不可读(应该是空的)

<br/>

## 逻辑运算符

xonsh 中同时支持 python 的 `and/or` 运算符和 bash 中的 `&&/||` 运算符, 其实本质上是把 `&&/||` 翻译成了 `and/or` 解析.

<br/>

## 转义

绝大部分情况都可以用字符串的形式实现对 xonsh 特殊语法的转义:

```bash
>>> print("$HOME")
$HOME
>>> echo "$HOME"
/Users/zhyipeng
>>> echo '$HOME'  # 由于 python 中单双引号意义一致, 所以 bash 中单引号转义的方式不适用
/Users/zhyipeng
>>> echo @("$HOME")  # 此时可用 @() 语法包裹
$HOME
>>> echo r'$HOME' # 有时候也可以用 r-string
$HOME
```

<br/>

## 字符串模式

### 高级字符串

xonsh 支持 python 的 r-string 和 f-string, 并且额外提供了一种在 shell 中很有用的 p-string

```bash
>>> p = p'/tmp'
>>> p
PosixPath('/tmp')
>>> type(p)
pathlib.PosixPath
```

> [pathlib](https://docs.python.org/3.8/library/pathlib.html) 是 python 标准库中的一个面向对象的文件系统路径的类, 大部分情况下可以代替 os.path 模块且更好用

大部分情况可以两两组合使用.

<br/>

### 路径正则

#### pythonic 正则

可以使用反引号(`)包裹字符串来做路径的正则匹配, 返回一个字符串形式的路径列表

```bash
>>> touch a aa a1 a2 aba cba
>>> `a\d+`
['a1',
 'a2']
>>> `~/a\w+`  # 绝对路径
['/Users/zhyipeng/aa',
 '/Users/zhyipeng/aba',
 '/Users/zhyipeng/cba']
>>> print(`a\d+`)
['a1', 'a2']
>>> ls `a\d+`  # 可以直接作为 subprocess 指令的参数而不需要使用 @(), 尽管它是个 list
a1 a2
```

> 更多正则语法参考 [re](https://docs.python.org/3/library/re.html) 模块

<br/>

#### bash 模式

subprocess-mode  下可以使用 bash 下的模式拓展:

```bash
>>> ls a*
a aa a1 a2 aba
>>> ls a[12]  # 中括号有特殊语法, 直接使用会有语法错误
SyntaxError...
>>> ls `a[12]`  # 此时应该使用 ` 
a1 a2
```

使用 g`` 语法可以将这种拓展适用在 python-mode 中:

```bash
>>> g`a*`  # 同样返回 list[str]
['a', 'aa', 'a1', 'a2', 'aba']
>>> ls g`a*`
a aa a1 a2 aba
>>> print(g`a*`)
['a', 'aa', 'a1', 'a2', 'aba']
```

<br/>

#### p-string

p`` 语法使用 pythonic 正则, 并且返回 list[Path]

```bash
>>> p`a\d+`
[PosixPath('a1'), PosixPath('a2')]
```

<br/>

## 帮助信息

ipython 中可以使用 `?` 和 `??` 获得对象, 函数, 类等的帮助信息, 对于纯 python 实现的方法,  `??` 还可能获得其源码.

当然, xonsh 也是支持的:

```bash
>>> import os
>>> os.path.join?
Type:         function
String form:  <function join at 0x10901d5e0>
File:         /usr/local/Cellar/python@3.8/3.8.6_2/Frameworks/Python.framework/Versions/3.8/lib/python3.8/posixpath.py
Definition:   (a, *p)
Docstring:
Join two or more pathname components, inserting '/' as needed.
If any component is an absolute path, all previous path components
will be discarded.  An empty last part will result in a path that
ends with a separator.


<function posixpath.join>
>>> os.path.join??
Type:         function
String form:  <function join at 0x10901d5e0>
File:         /usr/local/Cellar/python@3.8/3.8.6_2/Frameworks/Python.framework/Versions/3.8/lib/python3.8/posixpath.py
Definition:   (a, *p)
Source:
def join(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""
    a = os.fspath(a)
    sep = _get_sep(a)
    path = a
    try:
        if not p:
            path[:0] + sep  #23780: Ensure compatible data type even if p is null.
        for b in map(os.fspath, p):
            if b.startswith(sep):
                path = b
            elif not path or path.endswith(sep):
                path += b
            else:
                path += sep + b
    except (TypeError, AttributeError, BytesWarning):
        genericpath._check_arg_types('join', a, *p)
        raise
    return path



<function posixpath.join>
```

对 subprocess 命令使用 `?` 和 `??` 时则相当于 `man` 指令

```bash
>>> ls?
>>> ls??
>>> man ls
```

> 以上三个命令等价