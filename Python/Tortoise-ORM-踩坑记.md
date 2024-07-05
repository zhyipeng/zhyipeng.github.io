> Tortoise ORM是一个易于使用的 asyncio ORM，灵感来自Django。

## 为什么要用 tortoise-orm

- 稳定的异步 orm 框架选择不多
- django-like

<br/>

### 自动生成的表名

tortoise-orm 参考 django 的表名生成规则, 即直接把驼峰式的 Model 名 `lower()` (其实没抄全, django 默认还会附加上 app 名). 这个在新项目使用没什么问题, 但是如果需要对接已有项目, 而项目中的表名风格是下划线的, 比如 sqlalchemy 或者 xorm(go) 的项目, 使用自动生成的规则就很麻烦了, 总不可能每个 model 都去声明一下表名吧?

<br/>

在 models 源码找了半天没找到自动生成表名的源码, 经过各种 debug 终于发现它是在 Tortoise init 的时候 (居然是在 init_relations 里面!!! 这谁能想到? ) 遍历 model 赋值表名的... 只能说脑回路有点清奇了.

<br/>

虽然是找到了源码, 但是....

```python
@classmethod
def _init_relations(cls) -> None:
    def get_related_model(related_app_name: str, related_model_name: str) -> Type["Model"]:
        # 此处省略16行
        ...
    def split_reference(reference: str) -> Tuple[str, str]:
        # 此处省略20行
        ...
    
    for app_name, app in cls.apps.items():
        for model_name, model in app.items():
            if model._meta._inited:
                continue
            model._meta._inited = True
            if not model._meta.db_table:
                model._meta.db_table = model.__name__.lower()
    
    # 后面省略80+行
    ...
```

躲在这么个角落里, 重写也很麻烦啊... 要么 fork 一个分支出来改成支持自定义生成表名的方法, 要么另找他路. 考虑到作者都是尽量在往 django 方向靠拢, 应该不会考虑加上这么个功能(也不记得 django 有没有这样的功能了), 暂时还是考虑其他方案吧.

<br/>

这个地方是检查如果没有设置 db_table 则自动生成, 那么只需要在 init 之前把所有 model 赋上 db_table 就行. 给类自动附加属性的手段通常有几种:

- 基类
- 元类
- 类装饰器
- 后处理

前三个都需要对 model 本身的代码做改动, 或者对框架做 monkey patch, 都不是什么好方案, 所以还是考虑后处理吧. 只要在 models 定义完, 在 Tortoise init 前处理就行:

```python
import models
for m in dir(models):
    model = getattr(models, m)
    if isclass(model) and issubclass(model, Model) and not model._meta.abstract:
        if not model._meta.db_table:
            model._meta.db_table = camel_case_to_underline(model.__name__)
```

<br/>

### 水平分表

业务数据量上去之后分库分表是很常见的操作, 分库好说, orm 大都支持, 但是水平分表一般 orm 都没有直接支持.

> tortoise-orm 分库在官方文档的 examples 里就有

以常见的按日期分表为例, 之前用 sqlalchemy 我是这样办的:

```python
class AbsLog(Base):
    __abstract__ = True
    ...
    

def get_log_model(date: datetime.date) -> Type[AbsLog]:
    tablename = f'log{date.isoformat()}'
    
    class Log(AbsLog):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}
        # extend_existing 参数是在重复定义 Model 时以新的取代旧的. sqlalchemy 底层维护了一个表名到 model 的 map. 因此这里也可以从底层 map 中尝试获取, 或者自己维护缓存以复用 model
    
    return Log
```

用一个方法去动态生成对应的 Model.

<br/>

同样的思路用在 tortoise-orm:

```python
def get_log_model(date: datetime.date) -> Type[AbsLog]:
    tablename = f'log{date.isoformat()}'
    
    class Log(AbsModel):
        class Meta:
            table = tablename
    
    return Log
```

然后就报错了:

> tortoise.exceptions.ConfigurationError: No DB associated to model

model 没有关联 db? 那就给加上:

```python
def get_log_model(date: datetime.date) -> Type[AbsLog]:
    tablename = f'log{date.isoformat()}'
    
    class Log(AbsModel):
        class Meta:
            table = tablename
    
    Log._meta.default_connection = 'default'
    return Log
```

然后又报了另一个错:

> AttributeError: 'Query' object has no attribute '_select_field'

<br/>

回想一下上一个坑, tortoise-orm 会在 init 的时候遍历处理一遍 models, 可能在那时候还给 model 加了一些特效

<br/>

找了下果然有这么个方法:

```python
@classmethod
def _build_initial_querysets(cls) -> None:
    for app in cls.apps.values():
        for model in app.values():
            model._meta.finalise_model()
            model._meta.basetable = Table(model._meta.db_table)
            model._meta.basequery = model._meta.db.query_class.from_(model._meta.db_table)
            model._meta.basequery_all_fields = model._meta.basequery.select(
                *model._meta.db_fields
            )
```

<br/>

Find. 那就给动态生成的 model 也补上这些逻辑:

```python
def get_log_model(date: datetime.date) -> Type[AbsLog]:
    tablename = f'log{date.isoformat()}'
    
    class Log(AbsModel):
        class Meta:
            table = tablename
    
    Log._meta.default_connection = 'default'
    Log._meta.basetable = Table(tablename)
    Log._meta.basequery = Log._meta.db.query_class.from_(Log._meta.db_table)
    Log._meta.basequery_all_fields = Log._meta.basequery.select(*Log._meta.db_fields)
    return Log
```

完事, 可以正常获取到 Model 作查询了.

> 代码很丑陋, 可以再封装一下...