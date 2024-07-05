> 接口的三要素，入参、处理方法、出参。

## 一、获取参数

一般可以使用以下方法获取 Get 和 Post 参数

```go
this.Ctx.Request.PraseForm()
fmt.Println(this.CtxRequest.Form)
```



### 获取 queryparams

beego 会自动解析 queryparams 入参，可以通过以下方式获取数据：

- GetSeting(key string) string
- GetStrings(key string) []string
- GetInt(key string) (64int, error)
- GetBool(key string) (bool, error)
- GetFloat(key string) (float64, error)



```go
func (this, *MainController) Post() {
    username := this.GetString("username")
    if username == "" {
        this.Ctx.WriteString("username is empty.")
        return
    }
    
    // 如果需要非以上数据类型的入参
    age := this.Input().Get("age")
    intage, err := strconv.Atoi(age)
}
```



### 解析 body

首先需要在 app.conf 设置 `copyrequestbody = true`

```go
type User struct {
    Username string
    Age      int
}

func (this, *MainController) Post() {
    var user User
    var err error
    if err = json.Unmarshal(this.Ctx.Input.RequestBody, &user); err == nil {
        id := models.AddUser(user)
        this.Data["json"] = "{\"id\":" + id + "}"
    } else {
        this.Data["json"] = err.Error()
    }
    this.ServeJson()
}
```



> 通过 struct 可以初步对入参数据类型做校验



## 二、处理

只需要继承 beego.Controller 就可以成为一个 Controller(等价于 restframework 中的 ViewSet)，再给 controller 的方法加上注解路由(类似于 restframeword 的 action)就可以绑定上 url 和 http method 了

```go
type UserController struct {
    beego.Controller
}

// @router /user [get]
func (this *UserController) Get() {
    user := models.User{}
    _ := json.Unmarshal(this.Ctx.Input.RequestBody, &user)
    o := orm.NewOrm()
    _ := o.Read(&user)
    this.Data["json"] = &user
    this.ServeJSON
}
```

> 注解路由只是路由定义的其中一个较方便的方式



## 三、输出

要输出 json 形式的结果需要将结果保存为 struct

```go
func (this *AddController) Get() {
    mystruct := { ... }
    this.Data["json"] = &mystruct
    this.ServeJSON()
}
```