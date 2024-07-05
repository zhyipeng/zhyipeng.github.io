> beego 是 goland 最流行的框架之一。现开个坑，把博客用 beego + vue 重构了。之前是使用 django 做后端渲染，而我接下来的学习目标就是一个 go web 框架，和 vue，用这两个东西来实现前后端分离。

## beego/bee/beego orm

- beego: 一个很全面的 web 框架，定位类似 django，很多开箱即用的东西，这也是我选择它的原因，简单就好hhhhh（据说 gin 也不错，类比 flask）
- bee: beego 项目管理工具，用来创建、运行 beego 项目，类似 django-admin?
    - bee new/api => django-admin start project
    - bee run => python manage.py runserver
- beego orm: 作者的原话就是 "她的灵感主要来自 Django ORM 和 SQLAlchemy"

这样看来熟悉 django 的人应该能够很快的上手 beego 了。



## bee new/api

```bash
bee new [project name]
bee api [project name]
```

这两个命令是都是用来创建项目的，其中 new 是创建普通 beego 项目，即带 MVC 架构的后端渲染项目，而 bee api 则是创建一个接口专用的项目，区别主要在于一些配置的不同（如 autorender），以及是否有 views 模块



因为我的目标就是前后端分离项目，所以就直接 bee api 了。项目结构如下：

```bash
conf
	app.conf
controllers
	user.go
	object.go
models
	object.go
	user.go
routers
	router.go
tests
	default_test.go
main.go
```

- app.conf - 项目配置，同 django 的 settings.py 文件，可通过 beego.APPConfig 来访问配置项（django.conf.settings）
- controllers - 控制/视图层，内含一些示例代码
- models - 模型层，内含一些示例代码
- router.go - 路由配置
- tests - 单元测试
- main.go - 项目主文件



## Database

beego orm 连接数据库是需要手动调用 orm 的方法来连接的

```go
// 注册数据库驱动程序，driverName, driver
orm.RegisterDriver("mysql", orm.DRMySQL)

// 注册数据库, aliasName, driverName, dataSource
// beego orm 要求必须有一个 alias 为 default 的数据库作为主库
orm.RegisterDataBase("default", "mysql", "root:@/db_name?charset=utf8")

// 同步表结构，databaseName, force, verbose
// 类似 makemigrations & migrate，force 表示先执行 drop table，再 create，生产环境千万小心。
// 非 force 模式下，对于增删字段以及索引会自动处理，但是修改字段不会，需要手动处理，有点坑
// 除了在代码中执行同步，也可以在 shell 中做同样的操作：
// ./main orm syncdb -h [-force=false] [-db=default] [-v=false]
orm.RunSyncdb("default", false, true)
```



## Models

beego 构建模型除了语法是 go 之外，其他的几乎和 django 差不多：

看一下对比：

**Django**

```python
class Post(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    summary = models.TextField('摘要')
    body = models.TextField('正文')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    is_delete = models.BooleanField(default=False)

    tag = models.ManyToManyField('post.Tag', blank=True, verbose_name='标签')
    category = models.ForeignKey('post.Category', on_delete=models.SET_NULL, null=True, verbose_name='分类')
```

**Beego**

```go
type Post struct {
	Id int
	Title string
	Summary string `orm:"type(text)"`
	Body string `orm:"type(text)"`
	IsTop bool `orm:"default(0)"`
	IsDelete bool `orm:"default(0)"`
	CreatedAt time.Time `orm:"auto_now_add;type(datetime)"`
	UpdatedAt orm.DateTimeField `orm:"auto_now;type(datetime)"`

	Category *Category `orm:"null;rel(fk);on_delete(set_null)"`
	Tags []*Tag `orm:"rel(m2m)"`
}
```

> orm.DateTimeField 是继承了 time.Time 的结构的，它们在数据库对应的都是 datetime 类型。

有一份 go 数据结构对应到 mysql 数据结构的表：

| go                                          | mysql                           |
| ------------------------------------------- | ------------------------------- |
| int, int32 - 设置 auto 或者名称为 `Id` 时   | integer AUTO_INCREMENT          |
| int64 - 设置 auto 或者名称为 `Id` 时        | bigint AUTO_INCREMENT           |
| uint, uint32 - 设置 auto 或者名称为 `Id` 时 | integer unsigned AUTO_INCREMENT |
| uint64 - 设置 auto 或者名称为 `Id` 时       | bigint unsigned AUTO_INCREMENT  |
| bool                                        | bool                            |
| string - 默认为 size 255                    | varchar(size)                   |
| string - 设置 type(char) 时                 | char(size)                      |
| string - 设置 type(text) 时                 | longtext                        |
| time.Time - 设置 type 为 date 时            | date                            |
| time.Time                                   | datetime                        |
| byte                                        | tinyint unsigned                |
| rune                                        | integer                         |
| int                                         | integer                         |
| int8                                        | tinyint                         |
| int16                                       | smallint                        |
| int32                                       | integer                         |
| int64                                       | bigint                          |
| uint                                        | integer unsigned                |
| uint8                                       | tinyint unsigned                |
| uint16                                      | smallint unsigned               |
| uint32                                      | integer unsigned                |
| uint64                                      | bigint unsigned                 |
| float32                                     | double precision                |
| float64                                     | double precision                |
| float64 - 设置 digits, decimals 时          | numeric(digits, decimals)       |



模型定义完成后，就需要注册为数据表了，毕竟不像 python 那么方便，需要在 init 方法中调用 orm.RegisterModel 注册为数据表，注册之后 build 的时候就会自动响应 Syncdb 了

```go
func init() {
    orm.RegisterModel(new(Post), new(Tag), new(Category))
}
```