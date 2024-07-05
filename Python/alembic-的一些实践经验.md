> 一些实战经验

## 1. 动态修改配置
项目开发中常常将数据库链接写入环境变量或者配置文件中, 而 alembic 默认是从 ini 文件中读取配置的, 为了避免维护多份相同变量如数据库链接, 就需要在运行时动态地修改配置.

```python
# env.py
# 从项目配置中导入数据库链接
from setting_path import settings

config.set_main_option('sqlalchemy.url', settings.DB_URL)
```

## 2. 异步 DBAPI 支持

alembic 支持异步 api, 这在项目使用异步 DBAPI 时很有用

```bash
alembic init -t async [name]
```

## 3. 自动生成 migration 文件时避免删除手动创建的表

默认情况下 alembic 会尝试使 models 和数据库表完全同步, 当数据库中有手动创建的表时, alembic 会将其删除.

通常情况会建议避免手动创建表, 但是对于一些老项目或者多个程序维护的数据库, 亦或者分表的场景下, 手动创建表不可避免, 这时可以通过设置过滤方法使 alembic 不维护指定的表.

最简单且通用的方案就是只维护定义了模型的表: 

```python
def include_object(obj, name, type_, reflected, compare_to):
    if type_ == 'table' and reflected and compare_to is None:
        return False
    return True
	

# 在实际调用的 run_migrations 方法中修改 context.configure 的传参
context.configure(
		...
		include_object=include_object,
)
```

## 4. MacOS `._`文件问题

从 MacOS 复制项目到 Linux 时可能会带上 MacOS 生成的 `._` 开头的文件, 当 alembic 的 versions 目录下存在这些文件时会被 alembic 扫描到, 并且判断为异常的 version 文件, 导致 migrate 报错. 当存在这些文件时需要手动删除:

```bash
find . -type f -name '._*'
```