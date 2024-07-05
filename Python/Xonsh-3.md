> 类似其他shell, xonsh 在启动的时候会自动加载 `~/.xonshrc` 文件. 此文件使用 xonsh 的语法

本文将记录一些 `.xonshrc` 的一些常用配

类似其他shell, xonsh 在启动的时候会自动加载 `~/.xonshrc` 文件. 此文件使用 xonsh 的语法

本文将记录一些 `.xonshrc` 的一些常用配置

## 插件

xonsh 有着丰富的插件拓展功能, [社区](https://xonsh.github.io/awesome-xontribs/)也已经有不少成熟的插件了.

加载插件使用 `xontrib load` 命令, 那么在 `.xonshrc` 文件中合适的位置就可以自动加载已安装的插件了:

```python
xontrib load vox z sh
```
> vox 是 xonsh 专用的虚拟环境插件. 由于不完全兼容 bash 语法, pyenv 或者 virtualenv 直接在 xonsh 中使用会有些 bug, 所以有了这个插件去管理虚拟环境. 不过后文会提到另一种不适用插件的解决方案.
> z 是一款目录间跳转的插件
> sh 用于在 xonsh 中解析并执行 bash/zsh/fish 命令


## 环境变量

环境变量使用 python 变量声明语法, 但是变量名需要以 `$` 开头:

```python
$VI_MODE = True  # 设置 VI 模式
$PNPM_HOME = '/usr/local/bin'

$PATH.append($HOME + '/go/bin')  # $PATH 是个 list
del $PATH[$PATH.index('/usr/bin')]  # 删除某个值
```


## Prompt

之前介绍过 Prompt 的基本配置, 其实还有些小技巧

Prompt 里的变量除了预设的那些还可以添加自定义的, 并且这个变量可以是个方法, 会自动调用, 于是就有了这么个骚东西:

```python
import datetime

top_hours = '🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚'
half_hours = '🕧🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦'

# 自定义的变量定义在 $PROMPT_FIELDS 中
$PROMPT_FIELDS['time'] = lambda: half_hours[datetime.datetime.now().hour] if 15 < datetime.datetime.now().minute < 45 else top_hours[datetime.datetime.now().hour]

$PROMPT = '{#7f8c8d}{env_name}{BOLD_GREEN}{short_cwd}{branch_color}{curr_branch: {}}{RESET} {time} {RESET}'
```

每次执行完命令都会重新渲染 Prompt, 所以可以在方法中获取到当前时间并替换成对应的 emoji, 达到这样的效果:

```bash
~ 🕟
```

> ps: 类似 `import datetime` 在 `.xonshrc` 中引入的这些库在后续 xonsh shell 中就可以直接使用了.

## 自定义补全

定义一个自定义的补全很简单, 只要实现核心的补全方法就行了.

这里定义了一个自动补全 ssh 主机的补全器:
```python
from xonsh.completers.completer import add_one_completer


def parse_ssh_config():
    # 解析 ssh config 文件, 提取出所有的 host 列表
    hosts = $(grep Host\b ~/.ssh/config | awk '{print $2}' | grep '*' -v)
    return hosts.split('\n')


# 启动时把解析的结果保存到变量
$SSH_HOSTS = parse_ssh_config()


# 定义补全方法
def ssh_completer(prefix, line, begidx, endidx, ctx):
    if begidx != 0 and line.split(" ")[0] in ['ssh', 'scp']:
        return {i for i in $SSH_HOSTS if i.startswith(prefix)}


# 注册补全方法
add_one_completer('ssh', ssh_completer, '<cd')
```

## Python虚拟环境

我个人是喜欢用 pyvenv 的, 开箱即用. 所以稍微研究了一下搞了个兼容方法

```python
from pathlib import Path

def _newenv():
    """创建并进入虚拟环境"""
    python3 -m venv venv
    ./venv/bin/pip install jedi pylint  # 安装一些预设库
    source-bash venv/bin/activate  # activate 是 bash 脚本, 需要使用 source-bash 代替 source


def _exit_venv():
    """
    退出虚拟环境
    bash 下 activate 脚本会注册一个 bash 方法 deactive 去做这些事情,
    但是 xonsh 无法直接调用 deactive, 需要另外实现这个方法
    """
    # 找到当前环境的 python 所在目录
    p = Path($(which python)).parent
    # 删除 virtual env 相关的环境变量
    del $VIRTUAL_ENV
    del $VIRTUAL_ENV_PROMPT
    # 将虚拟环境从 $PATH 中移除
    $PATH.remove(str(p))


aliases['newenv'] = _newenv
aliases['venv'] = ['source-bash', './venv/bin/activate']
aliases['uvenv'] = _exit_venv
```