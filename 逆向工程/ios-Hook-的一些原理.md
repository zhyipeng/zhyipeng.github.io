> 抄的一些原理....

### 1. objective-c 方法调用流程

1. 在相应对象的缓存方法列表中 (objc_class 的 cache) 查找调用的方法
2. 如果没找到, 则在相应对象的方法列表中找调用方法
3. 如果还没找到, 就到父类指针指向的对象中执行前两步
4. 如果直到根类都没找到, 就进行消息转发, 给自己保留处理找不到方法这一状况的机会
5. 调用 resolvelnstanceMethod, 有机会让类添加这个函数的实现
6. 调用 forwardingTargetForSelector, 让其他对象执行这个函数
7. 调用 forwardlnvocation 更加灵活地处理函数调用
8. 如果通过以上操作都没有找到, 也没有进行特殊处理, 就抛出 doesNotRecognizeSelector


### 2. Method Swizzling
一个方法的实现是保存在IMP里面的. 同时, runtime提供了修改IMP的方法和交换两个IMP实现的方法. 通过交换两个 selector 的实现, 可以达到在调用A方法时实际调B方法, B方法里面可以继续调用A方法的效果, 通常把这种操作称为Method Swizzling.
Method Swizzling 在正向开发中可用于埋点, 数据监控统计, 防止crash 等等, 类似于 Python 装饰器的作用.
在逆向工程中可以通过对某个方法进行拦截和修改达到修改程序逻辑和数据的目的, objective-c 方法的 Hook 一般就是通过 Method Swizzling 实现的


### 3. Hook c 方法

[fishhook](https://github.com/facebook/fishhook) 是 FaceBook 开源的可以动态修改 MachO 符号表的工具。fishhook 的强大之处在于它可以 HOOK 系统的静态 C 函数。

C 函数在编译链接时就确定了函数指针的地址偏移量（Offset），这个偏移量在编译好的可执行文件中是固定的，而可执行文件每次被重新装载到内存中时被系统分配的起始地址是不断变化的, 因此并不能通过类似 Method Swizzling 的方式去 Hook C 函数.

> fishhook 利用了 MachO 的动态绑定机制: 苹果的共享缓存库不会被编译进我们的 MachO 文件，而是在动态链接时才去重新绑定。苹果采用了PIC（Position-independent code）技术成功让 C 的底层也能有动态的表现：
> 编译时在 Mach-O 文件 _DATA 段的符号表中为每一个被引用的系统 C 函数建立一个指针（8字节的数据，放的全是0），这个指针用于动态绑定时重定位到共享库中的函数实现。
> 在运行时当系统 C 函数被第一次调用时会动态绑定一次，然后将 Mach-O 中的 _DATA 段符号表中对应的指针，指向外部函数（其在共享库中的实际内存地址）。
> fishhook 正是利用了 PIC 技术做了这么两个操作：
> - 将指向系统方法（外部函数）的指针重新进行绑定指向内部函数/自定义 C 函数。
> - 将内部函数的指针在动态链接时指向系统方法的地址。
> 这样就把系统方法与自己定义的方法进行了交换，达到 HOOK 系统 C 函数（共享库中的）的目的。