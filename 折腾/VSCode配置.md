# VSCode配置

> 由于 Jetbrain 家的 IDEs 在我的 Mac M2 pro 上总是出渲染 bug, 一直查不到什么原因, 加上不太想用盗版了, 因此再一次尝试使用 VSCode 代替

开发需求:
- python
- go
- 前端(vue)
- 偶尔可能有些小需求 lua/squirrel

## 基建

### 基础的几个插件
- 语言包 - 没啥好说的
- 主题包 - 试了几个最后选择 Github Theme
- Keybindings - IntelliJ IDEA Keybindings, 更容易从 JB 过渡, 虽然还是有一堆要改的, 因为我在 JB 里也改了不少热键

### git
- GitLens - 被称为必备的 git 插件, 功能强大. 不过简单的 git 操作我更喜欢在终端用 lazygit
- Git Graph - GitLens 加上这个勉强可以和 JB 一战了

### 开发辅助
- Project Manager - 在侧边栏加上了一个项目目录, 可以快速切换项目, 其实也没啥大用, 聊胜于无
- Path Autocomplete - 自动补全路径, 补全相对路径很方便, 绝对路径貌似因为权限的问题无法识别
- Markdown All in One - 简单的文档就在 vscode 编辑, 复杂点的上 yn
- Todo Tree - 把代码里的 TODO/FIXME 等标志在侧栏的树状图中管理
- Excel Viewer - 使 VSCode 支持 Excel 文件查看/编辑

> Excel Viewer 容易误触编辑, 如果全局有自动保存配置的话就容易增加不必要的改动信息, 可以单独将 Excel 文件的自动保存关闭
> ```json
> {
>     "[excel]": {
>         "files.autoSave": "off"
>     },
> }
> ```

### AI
- github copilot - 收费, pass
- 通义灵码 - 阿里家的, JB 里用的这个, 勉勉强强吧, 但是在 VSCode 里它会给 Quick Fix 上下文菜单里加入 "使用通义灵码修复" 的项, 并且放到了第一个. 这个功能很鸡肋, 又严重影响调用其他 Quick Fix 功能的效率, 还找不到地方关闭, 所以 pass. (其他 AI 也会加入 Quick Fix, 但是没放第一位, 所以还好)
- 豆包 MarsCode - 字节的, 看到阮一峰推荐这个, 说和 github copilot 差不多水平了, 就想试试, 结果它在补全预览的时候拦截了 Esc 的行为, 严重影响 vim 的功能, 所以直接 pass.
- CodeGeeX - 清华大学的, 算是除了 github copilot 外我用过的体验最好的了

### vim
自从用了 vim 之后, 编辑器提供的编辑相关的热键都可以忽略了, 甚至非编辑相关的功能也可以绑到 vim 映射里

```json
{
    // vim 复制操作很多, 最好和系统剪贴板隔离开来, 避免污染系统剪贴板
    "vim.useSystemClipboard": false,
    // 使用 neovim
    "vim.enableNeovim": true,
    // easymotion 插件
    "vim.easymotion": true,
    // 使用相对行数
    "vim.smartRelativeLine": true,
    // 搜索相关的配置
    "vim.hlsearch": true,
    "vim.incsearch": true,
    // leader 键
    "vim.leader": "`",
    // 键绑定, 可以支持按键映射, 也可以调用 vscode 的功能
    // 功能 id 可以从 vscode 的热键配置里获取
    "vim.normalModeKeyBindingsNonRecursive": [
        // 移动 panel
        {
            "before": ["<leader>", "m"],
            "commands": ["workbench.action.moveEditorToNextGroup"]
        },
        {
            "before": ["<leader>", "M"],
            "commands": ["workbench.action.moveEditorToPreviousGroup"]
        },
        // 切换标签页
        {
            "before": ["J"],
            "commands": ["workbench.action.nextEditor"]
        },
        {
            "before": ["K"],
            "commands": ["workbench.action.previousEditor"]
        },
        // 切换 panel
        {
            "before": ["<leader>", "l"],
            "after": ["<C-w>", "l"]
        },
        {
            "before": ["<leader>", "h"],
            "after": ["<C-w>", "h"]
        },
        {
            "before": ["<leader>", "j"],
            "after": ["<C-w>", "j"]
        },
        {
            "before": ["<leader>", "k"],
            "after": ["<C-w>", "k"]
        },
        // 前进后退
        {
            "before": ["g", "h"],
            "commands": ["workbench.action.navigateBack"],
        },
        {
            "before": ["g", "l"],
            "commands": ["workbench.action.navigateForward"],
        },
        // 调用 easymotion
        {
            "before": ["s"],
            "after": ["<leader>", "<leader>", "s"],
        },
        // 最大化 panel
        {
            "before": ["<leader>", "f"],
            "commands": ["workbench.action.toggleMaximizeEditorGroup"]
        },
        // 打开最近的项目, 这是为什么说 Project Manager 插件鸡肋的原因
        {
            "before": ["g", "r"],
            "commands": ["workbench.action.openRecent"]
        },
        // git 常用操作
        {
            "before": ["g", "b"],
            "commands": ["git.checkout"]
        },
        {
            "before": ["g", "p"],
            "commands": ["git.pull"]
        },
        {
            "before": ["g", "P"],
            "commands": ["git.push"]
        },
        // 重构
        {
            "before": ["<leader>", "r"],
            "commands": ["editor.action.refactor"]
        }
    ],
}
```


## Python

动态语言的插件有点多

### 语言插件

- 语言插件 `Python` 
- 语言服务 `Pylanc`
- debugger `Python Debugger`

相关配置

```json
{
    "python.languageServer": "Pylance",
    // 启用类型检查
    "python.analysis.typeCheckingMode": "basic",
    // 使用自动完成器键入库时自动添加 import
    "python.analysis.autoImportCompletions": true,
    // 默认只会索引第三方库的第一层
    "python.analysis.packageIndexDepths": [
        {
            "name": "",
            "depth": 5
        },
    ],
    // 索引文件数量限制, -1 取消限制
    "python.analysis.userFileIndexingLimit": -1,
}
```

> 有点蛋疼的是第三方库的索引很多时候不完整, 常常要手动导入后才会被索引到, 暂时不知如何解决

### Linter&Formatter

然后就是代码格式化了, 包括 PEP8 格式化, 和导入优化 (删除未使用的导入), 此前可能需要几个插件来实现
- Flake8
- Black
- isort
- ...

但是现在有了更好的选择
- ruff - 使用 rust 写的高性能的 python linter 和 formatter

相关配置:
```json
{
    "[python]": {
        // 保存时自动格式化
        "editor.formatOnSave": true,
        // 使用 ruff 作为 formatter
        "editor.defaultFormatter": "charliermarsh.ruff",
        // 保存时的动作
        "editor.codeActionsOnSave": {
            // 优化导入排序
            "source.organizeImports": "explicit",
            // 删除未使用的导入
            "source.unusedImports": "explicit",
            // 尝试 fixAll
            "source.fixAll": "explicit"
        }
    },
    // ruff 全局配置, 此外还可以读取 project.toml 文件针对项目单独配置
    "ruff.configuration": "$HOME/.config/ruff/ruff.toml",
}
```

### 其他辅助插件

- autoDocstring - 自动生成标准格式化的 docstring
- Pip Manager - 在侧栏管理 pip 包, 但是 uv 创建的虚拟环境是没有 pip 的, 所以不太兼容
- Python Indent - 当输入 `Enter` 换行时可根据上下文设置更合适的缩进, 使用 vim-o 新增行时不适用

> python 项目会自动加载根目录下的 .env 文件里的环境变量, 在某些情况下会导致意想不到的 bug, 因此将它关掉: 
> ```json
> {
>     "python.envFile": "",
> }
> ```


## Go
相比 Python, Go 更开箱即用些, 装上 Go 插件, 设置一下 GOPATH 基本上就好了
```json
{
    "go.gopath": "$HOME/go"
}
```