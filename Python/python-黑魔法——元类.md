> 元类编程是 python 最大的黑魔法之一，很强大，但对于初学者来说确实难懂。我也是在项目中看同事用到，接手他的代码后才逐渐理解的，而他其实也是参考着 django 源码学的。所以这里就直接从 django 源码简单说一下元类的东西

## 元类是啥

我们知道 Python 中万物皆对象，对象是由类实例化来的，那类呢？也是个对象吗？

是的，与静态语言不同，python 中的函数、类都是在程序运行时由 python 解释器动态解析代码结构生成的 function 对象和 type 对象，这也是为什么你在单元测试模块里面瞎写一通格式错误也不影响到项目流程到原因，解释器压根没有解释到那里。

```python
>>> class A: pass
>>> type(A)
type
>>> def func(): pass
>>> type(func)
function
>>> a = A()
>>> type(a)
__main__.A
```

在创建类的时候，实际上是调用了 type 方法（实际上是调用 `type.__new__()`）

```python
A = type('A', (object,), {})
```

type 方法接收三个参数 type(name, base, attrs)：

- name  类的名字，即类的 `__name__` 属性
- base  基类(iter)
- attrs  类属性(dict)

> 区别于 type(obj) 查看对象的类型

所以，我们可以直接绕过类的定义式，在代码中直接使用 type 去创建一个类。

我们说创建类的类，就叫元类（MetaClass），而 type 就是最基础的元类



## 元类怎么用

元类需要继承 type，并且要重写 `__new__` 方法：

```python
# 定义元类
class MyMetaClass(type):
    def __new__(cls, name, base, attrs):
        # do something
        super_cls = super().__new__(name, base, attrs)
        # do something
        return super_cls
    

# 使用
class A(metaclass=MyMetaClass):
    pass
```

这样就可以在生成类的前后可以动态地给这个类绑上一些属性，虽然看起来是没什么用，直接给类写上对应的方法属性也是一样的。

那我们来举个栗子：

我们知道，django 的每个 Model 都会有 DoesNotExist 和 MultipleObjectsReturned 两个异常。按正常的思维，可能会在 Model 基类里去给到这两个类属性：

```python
class Model:
    class DoesNotExist(Exception):
        pass
    
    @classmethod
    def raise_does_not_exist(cls):
        if condition:
            raise cls.DoesNotExist
```

这样 Model 的子类也会有这两个异常，好像没什么不对。

再看这么个场景：

```python
class A(Model): pass
class B(Model): pass

try:
    A.raise_does_not_exist()
    B.raise_does_not_exist()
except A.DoesNotExist:
    print(A.__name__)
except B.DoesNotExist:
    print(B.__name__)
else:
    print('Nothing...')
```

这个时候你会发现无论 condition 是什么，要么会打印出 "A"，要么打印 "Nothing..."，并不会抛出 B.DoesNotExist 这种东西。

打印一下 A.DoesNotExist 和 B.DoesNotExist 会发现他们是同一个东西，所以始终会被第一个 except catch 掉。

但是这种场景在 ORM 框架中是很常见到的，我们需要给每个 Model 的子类都加上 DoesNotExist 的定义才行。我们看看 django 是怎么实现的：

```python
class ModelBase(type):
	 """Metaclass for all models."""
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        ...
        new_class = super_new(cls, name, bases, new_attrs)
        ...
        new_class.add_to_class('_meta', Options(meta, app_label))
        if not abstract:
            new_class.add_to_class(
                'DoesNotExist',
                subclass_exception(
                    'DoesNotExist',
                    tuple(
                        x.DoesNotExist for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (ObjectDoesNotExist,),
                    module,
                    attached_to=new_class))
            new_class.add_to_class(
                'MultipleObjectsReturned',
                subclass_exception(
                    'MultipleObjectsReturned',
                    tuple(
                        x.MultipleObjectsReturned for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (MultipleObjectsReturned,),
                    module,
                    attached_to=new_class))
            ...
        
        def add_to_class(cls, name, value):
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)
            
            
class Model(metaclass=ModelBase):
	...
```

没错，就是用的元类。它给每一个 cls 都加上了 DoesNotExist 属性，值是从 subclass_exception 方法构建的异常类。subclass_exception 方法的源码如下：

```python
def subclass_exception(name, parents, module, attached_to=None):
    """
    Create exception subclass. Used by ModelBase below.

    If 'attached_to' is supplied, the exception will be created in a way that
    allows it to be pickled, assuming the returned exception class will be added
    as an attribute to the 'attached_to' class.
    """
    class_dict = {'__module__': module}
    if attached_to is not None:
        def __reduce__(self):
            # Exceptions are special - they've got state that isn't
            # in self.__dict__. We assume it is all in self.args.
            return (unpickle_inner_exception, (attached_to, name), self.args)

        def __setstate__(self, args):
            self.args = args

        class_dict['__reduce__'] = __reduce__
        class_dict['__setstate__'] = __setstate__

    return type(name, parents, class_dict)
```

就是用 type 动态生成的一个 Exception 的子类。

这样子，每一个 Model 子类的 DoesNotExist 异常都可以单独 catch 了。



元类这东西就是让调用方用得更爽的东西，虽然实现方会写的很复杂。这种只有动态语言才能实现的黑科技在有些场景下会非常实用，但是也很容易造成意想不到的 bug，务必小心。

> django 源码是个好东西。。。。