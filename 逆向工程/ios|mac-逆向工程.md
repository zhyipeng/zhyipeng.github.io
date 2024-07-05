> 总结一些逆向的经验

### 1. 准备工具

1. [Hopper Disassembler](https://www.hopperapp.com/) - mac/linux 反编译工具, 功能类似 IDA, 比 IDA 便宜, 可以将汇编翻译成 OC 伪代码
2. [class-dump](https://github.com/nygard/class-dump) - 命令行工具, 可以从 Mach-O 文件生成 objective-c 头文件
3. [MonkeyDev](https://github.com/AloneMonkey/MonkeyDev/wiki) - Hook 框架, 同时支持越狱和非越狱式的 ios/mac Hook 开发, 集成了 class-dump, 恢复符号表, 重签名等功能
4. lldb - 经典动态调试工具, XCode 内置
5. [cycript](http://www.cycript.org/) - 通过进程注入, 使用 objective-c/javascript 语法, 可以直接调用程序内部方法
6. [reveal](https://revealapp.com/) - ios 运行时视图调试工具, 可以轻松地找到视图对应的 ViewController. 获取到的内存地址可以配合 cycript 食用 
7. usbmuxd/iproxy - 端口映射工具, 可以将 use 连接设备的某个端口(比如22)映射到宿主机(localhost)的指定端口
8. XCode - IDE
9. AppCode - Jetbrains 家的 objective-c IDE, 个人觉得写代码比 XCode 舒服
10. VSCode - 只有 VSCode 有 logos 语法插件, 写大段 logos 时需要


### 2. 基本流程

1. 砸壳, 获取 ipa
2. 使用 class-dump dump 出头文件, 或者拉到 MonkeyDev 跑一遍
3. 使用 reveal 获取到目标功能对应的 ViewController 类, 和实例的内存地址
4. 找到对应的头文件, 猜测相关的方法
5. 在 cycript 中调试猜测的方法
6. 如以上还无法推测出所需逻辑, 则在 Hopper/IDA 中查看方法的具体实现
7. 或者在 XCode 中打断点用 lldb 调试
8. 写 Hook 代码


### 3. cycript 基本使用

#### 安装
cycript 安装需要越狱设备, 在 Cydia 中安装即可

#### 注入
1. 推荐使用电脑 ssh 到 ios 设备操作
2. `ps -ef | grep xxx` 获取进程 id
3. `cycript -p 10086` 注入进程
4. done
5. C-D 退出交互式环境

#### 使用
```objective-c
// 创建对象
var view = [[UIView alloc] init]

// 从内存获取对象
var view1 = new Instance(0x1719f9a0)
var view2 = #0x1719f9a0

// 获取对象信息(以下皆可)
*view
[i for (i in *view)]
function tryPrintIvars(a){ var x={}; for(i in *a){ try{ x[i] = (*a)[i]; } catch(e){} } return x; }

// 访问对象属性
view.prop1
// 私有属性
view->_prop2

// 方法调用, oc/js 语法都可
[view viewDidLoad]
view.viewDidLoad()
```

> 参考: https://sevencho.github.io/archives/c12f47b1.html


### 4. lldb 简单使用
```bash
# 打印{表达式}
p {expression}

# 执行{表达式}
exp -- {expression}

```

> 参考: https://lldb.llvm.org/use/tutorial.html


### 5. logos 语法
MonkeyDev 同时支持 [CaptainHook](https://github.com/rpetrich/CaptainHook/) 和 [theos](https://github.com/theos/theos/wiki/Installation) Hook, 因此可以同时使用简洁的 [logos](http://iphonedevwiki.net/index.php/Logos) 语法和 OC 语法

```objective-c
// hook 声明, 自定类需要补充 interface
%hook NSBundle

+ (instancetype)bundleWithPath:(NSString *)path {
    // %log 会自动输出一些上下文信息
    %log;

    // %orig 调用并返回原方法
    return %orig;
}

- (NSString *)bundleIdentifier {
    return %orig;
}

// 动态添加方法
%new
- (void)addMethod {
    // %c 获取类(objc_getClass)
    %c(ClassName)
}

// hook 截止声明
%end
```