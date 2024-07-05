> objective-c 是一门面向对象语言, 在 swift 出现之前一直统治着 macOS 和 ios 的软件开发. 它是 c 语言的超集, 完全向下兼容 c 的语法, 

### 1. HelloWorld

```objective-c
@interface Demo : NSObject
- (void)helloWorld:(NSString *)name;
@end

@implementation Demo
- (void)helloWorld:(NSString *)name {
    NSLog(@"hello %@", name);
}
@end

// main
Demo *demo = [[Demo alloc] init];
[demo helloWorld:@"objective-c"];

```

### 2. 文件类型

- .h - 头文件
- .m - 源代码文件, 同时支持 OC 和 C 语法
- .mm - 源代码文件, 同时支持 OC/C/C++ 语法


### 3. 语法糖 & 关键字

OC 中使用 "@" 来区分 OC 语法特征和 c 语法特征

- @interface - 声明接口
- @implementation - 声明实现
- @end - 代码块结束
- @class - 声明类
- @property - 声明类的属性, 自动实现 get/set 方法
- @synthesize - property 的实现
- ...


### 4. 变量类型

OC 向下兼容所有 c 变量类型, 如 int, long long, bool 等...

此外 OC 还定义了一些特殊的数据结构:

- NSString
- NSNumber
- BOOL
- NSObject
- NSData
- NSDictionary
- NSArray
- NULL
- ...


可通过调用 init 方法创建对象, 更多的时候是使用 @ 声明.
```objective-c
NSString *str = @"string";
NSNumber *num = @(11);
NSNumber *num1 = @(11.1);
BOOL t = YES; // NO
NSDictionary *dict = @{
    @"key1": @"value1",
    @"key2": @{
        @"key21": @(1)
    },
    @"key3": @[@"v1", @"v2"]
};
NSArray *list = @[@(1), @(2)];
```

> NSArray / NSDictionary 内部只能是 OC 对象

> NSArray / NSDictionary 不可变, 但是有 NSMutableArray / NSMutableDictionary
> 是可变的


### 5. 类

**声明类**

```objective-c
@interface Demo : NSObject
@end

@implementation Demo
@end
```

**声明对象**
```objective-c
// 分配空间
Demo *demo = [Demo alloc];
// 初始化
demo = [demo init];


// 或者 new 关键字, 两种方式等价
Demo * demo = new Demo *;
```

> 如果需要重写对象的初始化行为, 可重写 init 方法, 也可以定义额外的 init 方法, 显式地通过 alloc - myinit 去创建对象


**类属性**

```objective-c
@interface Demo : NSObject

// 通过 property 声明
@property (readonly, weak) NSString *prop1;
@property BOOL prop2;

- (void)setProp3:(NSString *)prop3;
- (NSString *)getProp3;

@end

@implementation Demo {
    // 声明私有属性, 然后通过调用 get/set 方法访问
    NSString *_prop3;
}

@synthesize prop1;
@synthesize prop2;

- (void)setProp3: (NSString *)prop3 {
    self->_prop3 = prop3;
}

- (NSString *)getProp3 {
    return self->_prop3;
}

@end
```

> . 和 -> 都可以访问对象属性, 区别在于 . 是调用属性的 set/get 方法, 而 -> 是直接访问属性本身

property 可以设置一些属性(\*表默认): 
- atomic\* / nonatomic - 是否增加事务锁(多线程), 如果无多线程的情况, 手动加 nonatomic 可提高效率
- readwrite\* / readonly - 只读时不会生成 setter 方法
- strong\* / weak - 强/弱引用, strong 时会增加对象的引用计数
- assign\* / copy / retain - 赋值行为, assign 直接赋值, 不改变引用计数; retain 拷贝指针, 并释放旧的对象; copy 拷贝内容, 并释放旧的对象
- getter / setter - 手动设置 get/set 方法


**方法**
```objective-c
@interface Demo : NSObject
- (void)method1;
+ (NSArray<NSString *> *)sort: (NSArray<NSString *> *)array;
+ (NSArray<NSString *> *)sort: (NSArray<NSString *> *)array reverse:(BOOL)reverse;
@end

@implementation Demo
- (void)method1 {
    return;
}
+ (NSArray<NSString *> *)sort: (NSArray<NSString *> *)array {
    // ...
    return array;
}
+ (NSArray<NSString *> *)sort: (NSArray<NSString *> *)array reverse:(BOOL)reverse {
    // ...
    return array;
}
@end
```

`+/- (returnType)MethodName:(argType)argName MethodName:(argType)argName...`
- \+ 声明类方法, - 声明对象方法
- OC 中方法名可理解为是调用参数的一部分, 因此声明的时候方法名是割裂开的
- 方法签名是包含完整方法名的, 并且用:标识参数, 如以上方法签名分别为: method1 / sort: / sort:reverse:


**方法调用**

```objective-c
Demo *demo = [[Demo init] alloc];
[demo method1];
[Demo sort:@[@"a", @"b"]];
[Demo sort:@[@"a", @"b"] reverse:YES];
```


### 6. 导入头文件

C 中的 include 语法仍然适用, 但是 OC 定义了更佳的 import 语法:
```objective-c
#import "xxx.h"
#import <xxx.h>
```

如果在头文件需要使用其他文件的类时, 则需通过 `@class` 引入
