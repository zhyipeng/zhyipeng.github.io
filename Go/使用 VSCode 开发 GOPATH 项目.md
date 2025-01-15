# 使用 VSCode 开发 GOPATH 项目

高版本 go 默认使用 go mod 了，vscode 的 go 插件也是默认支持的，反而以前的 GOPATH 项目不能默认支持了，需要做一些特殊配置

具体如下：
> 建议配置在项目配置中

```json
{
    "go.goroot": "$GOROOT",
    "go.gopath": "$(pwd)",
    "go.toolsEnvVars": {
        "GO111MODULE": "off",
        "GOPATH": "$(pwd)"
    },
}
```

在 vscode 中这样配置就 ok 了，但是在 cursor 中有点问题：
在终端里的 go 并不是 settings.json 中的 go.goroot，疑似 vsc 的 go 插件会自动加载 goroot 进终端，而到了 cursor 有点水土不服？

未深究其原因，覆写一下终端环境变量完事：

```json
"terminal.integrated.env.osx": {
    "PATH": "$GOROOT/bin:$PATH"
}
```

