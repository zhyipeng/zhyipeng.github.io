> 列举一些项目中出现的高级查询

## 更新指定字段
django orm:
```python
User.objects.filter(id=1).update(name='name')
// or
user.name = 'name'
user.save(update_fields=('name',))
```
beego orm:
```go
user := models.User{Id: 1, Name: "name", Age: 12}
o := orm.NewOrm()
o.Update(&user, "Name", "Age)
```

## 查询指定字段
### 单实例查询
django orm:
```python
user = User.objects.filter(id=1).only('id', 'name').first()
```
beego orm:
```go
user := User{Id: 1}
o := orm.NewOrm()
o.Read(&user, "Id", "Name")
```



----
Django ORM 中的 Model.save() 方法其实很好用，所以我在项目中也实现了一个简单的 ModelSave 接口：
```go
type BaseModelInterface interface {
	GetPrimaryKey() int
	SetPrimaryKey(int)
}

func ModelSave(i BaseModelInterface, updateFields ...string) (err error) {
	o := orm.NewOrm()
	if i.GetPrimaryKey() == 0 {
		id, err := o.Insert(i)
		if err == nil {
			i.SetPrimaryKey(int(id))
		}
	} else {
		_, err = o.Update(i, updateFields...)
	}
	return
}
```
这样更新的时候：
```go
func (user *User) SetDeleted() {
  user.IsDeleted = true
  // user.save(update_fields=['isDeleted'])
  ModelSave(&user, "isDeleted")
}
```
创建的时候：
```go
func (user *User) CreateUser(u *User) {
    // user.save()
    ModelSave(&user)
}
```
