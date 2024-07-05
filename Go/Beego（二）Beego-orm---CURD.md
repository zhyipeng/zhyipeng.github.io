> CURD 是基本功...

## 简单的 CURD

### Create

**create one**

```go
o := orm.NewOrm()
var user User
user.Username = "xiaoming"
user.Password = "123456"

id, err := o.Insert(&user)
if err == nil {
    fmt.Println(id)
}
```



**create batch**

```go
users := []User{
	{Username: "xiaoming"},
	{Username: "xiaobai"},
	{Username: "dabai"}
}
successNums, err := o.InsertMulti(3, users)		// 第一个参数为分批创建的size，而不是总数量
```



### Read

**read one**

```go
o := orm.NewOrm()
user := User(Id: 1)   // 通过主键查询

err := o.Read(&user)

if err == orm.ErrNoRows {
    fmt.Println("None")
} else if err == orm.ErrMissPK {
    fmt.Println("ObjectNotFound")
} else {
    fmt.Println(user.Id, user.Name)   // 查询结果会赋值给 user
}

user := User(Username: "xiaoming")   // 通过其他字段查询
err := o.Read(&user)
...
```



**read all**

```go
o := orm.NewOrm()
users := []User
qs := o.QueryTable("user")
total, err := qs.All(&users)
if err == nil {
	fmt.Println(total)
}
```



**read or create**

```go
o := orm.NewOrm()
user := User{"Username": "xiaoming"}

// 至少传入一个参数作为查询条件字段
if created, id, err := o.ReadOrCreate(&user, "Username"); err == nil {
    if created {
        fmt.Println("New Object. Id: ", id)
    } else {
        fmt.Println("Get an object. Id: ", id)
    }
}
```



### Update

```go
o := orm.NewOrm()
user := User{Id: 1}
if o.Read(&user) == nil {
    user.Username = "xiaohong"
    if num, err := o.Update(&user); err == nil {
        fmt.Println(num)
    }
}
```



### Delete

```go
o := orm.NewOrm()
if num, err := o.Delete(&User{Id: 1}); err == nil {
    fmt.Println(num)
}
```

> Delete 方法支持表关联级联操作



## 使用 SQL 语句查询

参考 [使用sql语句进行查询](https://beego.me/docs/mvc/model/rawsql.md#使用sql语句进行查询)



## QuerySet 查询

参考 [高级查询](https://beego.me/docs/mvc/model/query.md#高级查询)



## 更复杂的查询

如需更复杂的查询，如 子查询和多重联结等，参考 [构造查询](https://beego.me/docs/mvc/model/querybuilder.md#构造查询)



## 事务处理

```go
o := orm.NewOrm()
err := o.Begin()
...
...
if SomeError {
    err = o.Rollback()
} else {
    err = o.Commit()
}
```