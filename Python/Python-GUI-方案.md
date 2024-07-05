> 脚本写多了, 难免会有 GUI 化的需求, 本文就简要介绍一些常见的 GUI 方案.

# Python GUI 方案

脚本写多了, 难免会有 GUI 化的需求, 本文就简要介绍一些常见的 GUI 方案.

## 正经 GUI

### Tkinter
标准库中的 GUI 库, 最大的优势在于装了 Python 的电脑就能用, 除此之外几乎没啥亮点了, 界面丑, api 低级, 要啥没啥. 不过写个小工具什么的还是问题不大的.

也有不少尝试给 tkinter 造 designer 工具的, 其中做得比较好的有个基于 Figma 的 [Tkinter-Designe](https://github.com/ParthJadhav/Tkinter-Designer), 在这些工具的加持下 tkinter 的开发会简单很多, 界面也会好看一些, 但是用的人相对少, 对于大工程所需要的各种功能还是需要手撕轮子.

同类 gui 库还有个第三方的 wxPython.

### PyQT/PySide
qt 系可以说是 Python 桌面 GUI 方案中的天花板了. 界面用 QTDesigner 画, 样式有类似 CSS 的 QSS, 然后 python 快速写业务, 性能瓶颈用 c++ 无缝连接, 生态完善.

缺点的话, qt 收费, 但是 PySide 免费, 基本可以无缝替代. 以及生态比较重, 打包体积大, 更适合生产力工具的开发.


### 高度封装的库

#### [Guietta](https://github.com/alfiopuglisi/guietta)
这是个脑洞很大的库, 它对 pyqt 的 api 做了封装, 封装成了一组神奇的 api, 它的 demo 长这样:

```python
from guietta import _, Gui, Quit
gui = Gui(
	[ "Enter numbers:",  "__a__", "+", "__b__", ["Calculate"] ],
	[    "Result: -->", "result",   _,       _,             _ ],
	[                _,        _,   _,       _,          Quit ]
)

with gui.Calculate:
	gui.result = float(gui.a) + float(gui.b)

gui.run()
```

出来效果是这样的:
![Img](https://camo.githubusercontent.com/ec60435d6c58247c9f4bdec744a1461d31f68b4c3ccf5c809c0be12c35bda4c9/68747470733a2f2f677569657474612e72656164746865646f63732e696f2f656e2f737461626c652f5f696d616765732f6578616d706c652e706e67)

达成了"真·所见即所得". 脑洞很大, 但是实用性有限, 功能很少, 只适合快速做一些小工具.

#### [PySimpleGUI](https://github.com/PySimpleGUI)
PySimpleGUI 则是对 tkinter, QT, WxPython, Remi 四个 gui 库的 api 封装成了同一套, 使用时可以灵活选择不同的 gui 平台来达到更好的效果, 节省不同 gui 生态之间的迁移成本.

目前似乎也没有配套的 designer 软件, 需要手写界面. 没有深入了解, 不知道能否直接使用 QT 的 ui 文件, 就算能用, 那为什么不直接用 PyQT 呢?
 

## TUI

TUI 是指基于终端实现的图形界面, 主要依靠字符拼接来实现图像效果. 由于运行在终端, 会更重键盘输入而轻(无)鼠标输入.

TUI 软件里最常见的就是 linux 下的 top 和 vim. Go 实现的 [lazygit](https://github.com/jesseduffield/lazygit) 和 [lazydocker](https://github.com/jesseduffield/lazydocker) 也很好用, 这两是使用 [gocui](https://github.com/jroimartin/gocui) 实现的. 

python 生态下的 TUI 软件比较少, 但是也有和 gocui 类似的库: (py_cui)[https://github.com/jwlodek/py_cui]

python 更擅长的是在交互式软件中提供更好看的输出, 更具交互性的操作, 这也和自身身为脚本语言的特性一脉相承. 这一类软件的典型代表是 ipython, mycli, iredis...

用于交互式软件中的辅助库也有不少好用的:

- [rich](https://github.com/Textualize/rich) - 提供富文本和精美的输出, 还可以绘制漂亮的表格，进度条，markdown，突出显示语法的源代码及回溯等等.
- [tqdm](https://github.com/noamraph/tqdm.git) - 专注于输出好看的进度条

## 基于 web 技术

基于 web 的 gui 方案是现代化 gui 中重要的一部分. 应用程序运行在浏览器上, 所以可以轻易地做到跨平台. web 技术目前还离不开 javascript (WASM 有望在未来替代掉一部分的 js), 所以这类方案基本上是使用 js 构建 ui, 然后使用其他技术去写逻辑, 本质上是一个前后端分离的方案.


### 传统web
即使用 html/css/js 构建网页 ui, python 做服务端写业务逻辑, 通过 http/websocker 协议传输数据和操作.

### [PyWebIkO](https://github.com/pywebio/PyWebIO)
pywebio 实际上是基于传统 web 的, 它的服务端使用 websocker 主动向客户端推送指定格式的消息(或者客户端向服务端轮询), 客户端接受到消息后按照一定的规则去进行 dom 操作, 从而实现 ui 的动态更新, 甚至是局部刷新.

利用此框架, 可以完全不需要编写前端代码即可实现简单的 web 页面.

### [electron](https://www.electronjs.org/)
electron 是应用最广泛的使用 web 技术构建桌面级应用的框架了. VSCode, 飞书, 钉钉, 网易云桌面端等等一众桌面软件都是使用 electron 构建的.

但是由于每个程序都要打包进一个浏览器, 导致程序体积和内存占用比其他的app更大, 并且渲染性能瓶颈也在于浏览器的 js 引擎, 还是比原生程序差了不少的.

技术分配上和传统 web 类似, 可以独立运行服务端做成网络软件, 或者把 python 程序和 python 解释器也一同打包 (体积更大了).

### [pyscript](https://pyscript.net/)
pyscript 号称在浏览器上直接运行 python 代码, 本质上是将 python 代码解析为 WASM, 再由浏览器直接执行.

pyscript 现阶段还无法替代 javascript 操作 DOM 的功能, 只能用于写业务逻辑. 其最大的意义在于将 python 生态的第三方库引入到浏览器中, 而无需使用 C-S 架构.


## 不正经的 GUI

### [Rumps](https://github.com/jaredks/rumps)
rumps 用于构建 macOS 的菜单栏软件, 其原理是对 PyObjC 进行了封装, PyObjC 将 python 代码编译为 objective-c 代码, 然后构建出 macOS 应用.

缺点: macOS 独占

exp:[一个纯粹的ssh隧道工具](git@github.com:zhyipeng/itunnel.git)


### [aardio](https://www.aardio.com/)
和 web 中使用 js 调用 python api 类似, 这个方案则是用一个名为 aaradio 的语言写界面并调用 python 脚本. 

优点: 界面拖拽生成, 社区有不少常见范例的解决方案, aardio 本身是一个比 python 还简单的脚本语言, 堪比易语言/vb. 

缺点: 闭源, windows 独占, 编译器内置的 python 是 winpython3.4, 不知道能否自行替换使用更高版本的 python.

