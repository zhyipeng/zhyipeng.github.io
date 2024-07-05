> 

# Xonsh-2


## Aliases

在 bash 中可以通过 alias 设置命令别名
```bash
>>> alias l=ll
```

而在 xonsh 中, 不再兼容这种写法, 而是维护一个类字典的映射结构 `aliases`, 通过字典的语法来添加/删除alias
```bash
>>> aliases['l'] = 'll'
>>> aliases['ll'] = ['ls', '-l']
# 也可以为xonsh语法设置别名, 并通过 $args/$arg<n> 获取传参
>>> aliases['piu'] = 'pip install -U @($args)'
aliases['cdls'] = 'cd $arg0 && ls'
```

### 可调用的别名

如果 aliases 值是一个函数, 则会自动动调用该函数
```python
>>> def mycmd0():
>>>     return 'hello world'
>>> aliases['cmd0'] = mycmd0
>>> cmd0
hello world
```

函数可以接受调用参数
```python
def mycmd1(args):
    # 当定义单个参数时, 会将传参以 list[str] 的形式传入
    return ','.join(args)


def mycmd2(args, stdin=None, stdout=None, stderr=None, spec=None, stack=None):
    # 后面这些参数都是可选的, 传入的值应该看名字就看得出来是个啥了
    pass
```

## Prompt
一款完备的 shell 肯定是要支持自定义 Prompt 格式的.

```bash
>>> $PROMPT = '{user}@{hostname}:{cwd} > '
snail@home:~ > # it works!
snail@home:~ > $PROMPT = lambda: '{user}@{hostname}:{cwd} >> '
snail@home:~ >> # so does that!
```

默认情况下, 可以使用以下变量:

- `user`: 当前用户名
- `hostname`: 主机名
- `cwd`: 当前工作目录, 可以使用 `$DYNAMIC_CWD_WIDTH` 定义此变量的最大宽度, 使用 `$DYNAMIC_CWD_ELISION_CHAR` 定义超出最大宽度时的缩略符
- `short_cwd`: `cwd`的缩写形式, 例如 `/path/to/xonsh` -> `/p/t/xonsh`
- `cwd_dir`: 当前工作目录的父目录
- `cwd_base`: 当前工作目录的名字
- `env_name`: 活动虚拟环境的名称(如果有的话). 此变量的效果受 `$VIRTUAL_ENV_PROMPT` 和 `$VIRTUAL_ENV_DISABLE_PROMPT` 变量的影响, 具体后面详述
- `env_prefix`: 虚拟环境的前缀字符, 默认为 "("
- `env_postfix`: 虚拟环境的后缀字符, 默认为 ")"
- `curr_branch`: 当前 git 分支名(如果有的话)
- `branch_color`: 颜色. 如果当前分支是干净的, 则默认为 `{BOLD_GREEN}`, 否则为 `{BOLD_RED}`, 如果无法确定, 则为黄色
- `branch_bg_color`: 同上, 但是是背景色
- `prompt_end`: 如果用户具有 root 权限则为 `#`, 否则为 `$`
- `current_job`: 当前在前台运行的命令名称(如果有的话)
- `vte_new_tab_cwd`: 发出 VTE 转义序列, 用于在某些 linux 终端的当前工作目录中打开新的选项卡. 通常不需要.
- `gitstatus`: 和 `[main|MERGING|+1...2]`一样, 可以引用 `xonsh.prompt.gitstats` 来自定义
- `localtime`: `time.localtime()`给定的当前本地时间, 并使用 `time_format` 格式化
- `time_format`: 时间格式字符串, 默认为 `%H:%M:%S"
- `last_return_code`: 上次命令的返回码
- `last_return_code_if_nonzero`: 同上, 但只有非零才有值

> Xonsh 服从 viralenv 定义的 `$VIRTUAL_ENV_DISABLE_PROMPT` 环境变量。如果该变量为 true，xonsh 将始终用空字符串替换 `{env_name}` 。
> 注意，与其他 shell 不同， `$VIRTUAL_ENV_DISABLE_PROMPT` 在设置后立即生效ーー不需要重新激活环境。
> Xonsh 还允许通过 `$VIRTUAL_ENV_PROMPT` 环境变量显式覆盖 `{env_name}` 的呈现。
> 如果定义了此变量并且该变量具有 None 以外的任何值，则在激活环境时， `{env_name}` 将始终呈现为 `str($VIRTUAL_ENV_PROMPT)` 。当没有环境处于活动状态时，它仍将呈现为空字符串。 `$VIRTUAL_ENV_PROMPT` 被 `$VIRTUAL_ENV_DISABLE_PROMPT` 重写。

