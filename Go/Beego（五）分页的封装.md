> 列表接口分页是非常有必要的。Beego 没有提供分页接口，文档给的示例看起来也很难受，那就自己封装一个吧。

主要思路是参考 django-restframework

- paginate_queryset 方法可以从请求参数中提取出分页参数，并对传入的 queryset 对象加上分页查询
- get_paginated_response 方法可以对已做分页的查询返回包装了分页参数的响应数据
- 应该兼容未传分页参数的情况

有了思路，就可以撸起袖子干了

## PaginateQuerySet
Pagination 主要负责对分页相关方法的封装
```go
type Pagination struct {
	QuerySet orm.QuerySeter
	Page     int
	Size     int
}
```

在有了这些参数的情况下 paginate_queryset 方法很简单了
```go
func (p *Pagination) PaginateQuerySet() orm.QuerySeter {
	return p.QuerySet.Limit(p.Size, p.Size*(p.Page-1))
}
```

这个时候已经可以从 Controller 去实现分页查询了，只要提取出分页参数，然后 new 一个 Pagination，就可以调方法查了。

为了更好用，可以把上述步骤也在 BaseController 里抽象一下

首先应该在 BaseController 加上一些私有属性用来保存分页属性
```go
type BaseController struct {
	beego.Controller
	paginator Pagination
	HasPage   bool
}
```
再实现 BaseController 的 PaginateQueryset 方法
```go
func (this *BaseController) PaginateQuerySet(qs orm.QuerySeter, focus bool) orm.QuerySeter {
	page, err := this.GetInt("page")
	if err != nil {
        // focus 用来控制是否强制要求分页，如果不是则返回原 queryset，否则给默认分页参数
		if !focus {
			return qs
		}
		page = 1
	}
	size, err := this.GetInt("size")
	if err != nil {
		if !focus {
			return qs
		}
		size = 10
	}
	this.HasPage = true
	this.paginator = Pagination{QuerySet: qs, Page: page, Size: size}
	return this.paginator.PaginateQuerySet()
}
```

至此，调用方就可以简单地对查询进行分页了：
```go
func (this *UserController) GetUsers() {
	o := orm.NewOrm()
    qs := o.QueryTable("user").Filter("IsDeleted", false).OrderBy("-CreatedAt")
    qs = this.PaginateQueryset(qs, true)
  ...
}
```

## GetPaginatedResponse

beego 中构造接口返回结构最简单的方法就是传入一个 struct 了，所以我们先来构建一个 PaginatedResponse 结构：

```go
type PaginatedResponse struct {
	PageInfo PageInfo    `json:"page_info"`
	Data     interface{} `json:"data"`
}

type PageInfo struct {
	CurrentPage int   `json:"current_page"`
	Total       int64 `json:"total"`
	LastPage    int   `json:"last_page"`
}
```

然后给 Pagination 加上 GetPaginatedResponse 方法
```go
func (p *Pagination) GetTotalPages(total int64) int {
	if p.Size == 0 {
		return 0
	} else {
		return int(math.Ceil(float64(total) / float64(p.Size)))
	}
}

func (p *Pagination) GetPaginatedResponse(data interface{}) (PaginateResponse, error) {
	// data 需要是空接口类型，保证可以传入不同 model 的数据列表
    total, err := p.QuerySet.Count()
	if err != nil {
		return PaginateResponse{}, err
	}
	page := PageInfo{CurrentPage: p.Page, Total: total, LastPage: p.GetTotalPages(total)}

	return PaginateResponse{PageInfo: page, Data: data}, err
}
```

同理，还是在 BaseController 里封装多一层
```go
func (this *BaseController) GetPaginatedResponse(data interface{}) (PaginateResponse, error) {
	return this.paginator.GetPaginatedResponse(data)
}
```

完事
```go
func (this *UserController) GetUsers() {
    ...
    // 同时支持分页和不分页
    if this.HasPage {
		this.Data["json"], _ = this.GetPaginateResponse(users)
	} else {
		this.Data["json"] = users
	}
	this.ServeJSON()
}
```


