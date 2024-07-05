> python 作为解释型语言, 有着很方便的交互式 shell 做调试. debug 过程中往往需要经常修改代码, 如果每次都需要重新进入 shell 的话就很麻烦. 不过如此灵活的语言自然有应对方法....

## 1. importlib
[文档](https://docs.python.org/zh-cn/3/library/importlib.html)

> importlib 包的目的有两个。 第一个目的是在 Python 源代码中提供 import 语句的实现（并且因此而扩展 __import__() 函数）。 这提供了一个可移植到任何 Python 解释器的 import 实现。 相比使用 Python 以外的编程语言实现方式，这一实现更加易于理解。

>第二个目的是实现 import 的部分被公开在这个包中，使得用户更容易创建他们自己的自定义对象 (通常被称为 importer) 来参与到导入过程中。

importlib 提供了 reload 方法以避免每次更改代码后都必须重新启动交互式会话

```python
>>> import func from module
>>> func()
"This is result..."
# Make some changes to "func"
>>> func()
"This is result..."  # Outdated result
>>> from importlib import reload; reload(module)  # Reload "module" after changes made to "func"
>>> func()
"New result..."
```


## 2. ipython

> IPython是一种基于Python的交互式解释器。相较于本地的Python Shell，IPython提供了更为强大的编辑和交互功能。

ipython 提供了一系列魔法指令, 其中便有一条是关于自动重载的 [autoreload](https://ipython.org/ipython-doc/3/config/extensions/autoreload.html)

```python
In [1]: %load_ext autoreload

In [2]: %autoreload 2

In [3]: from foo import some_function

In [4]: some_function()
Out[4]: 42

In [5]: # open foo.py in an editor and change some_function to return 43

In [6]: some_function()
Out[6]: 43
```

可以将这两天语句放入配置中, 每次进入 ipython 自动加载 autoreload
```shell
echo "c.InteractiveShellApp.exec_lines = [ '%load_ext autoreload', '%autoreload 2' ]" >> ~/.ipython/profile_default/ipython_config.py                                                        <
```
