> 后端渲染新姿势...


## 为什么要引入vue

归根结底是要减少前端开发成本. 项目使用 flask-admin 已经大幅度减少了前端代码量了, 只有一些复杂需求才需要编写前端代码. 

当不可避免地需要手写前端的时候, 那就引入框架来减少开发成本吧. 通常后端渲染的解决方案是 jq, 但是用过 vue 后就不再想用 jq 了, 操作 DOM 还是比较蛋疼... 而且 vue 组件库可比 flask-admin 的 Bootstrap 要好用得多(虽然不是同个概念的东西)

那就来看看怎么引入 vue 吧

## 如何结合

首先既然是 Jinja2 模板式渲染的话就不能用 vue 工程的形式了, 那就简单粗暴地用 CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
```

或者把源文件放项目里引入


```html
{% block head_tail %}
    <script src="https://cdn.jsdelivr.net/npm/vue"></script>
{% endblock %}

{% block body %}
    <div id="app">
    </div>
{% endblock %}

{% block tail_js %}
    <script>
        var app = new Vue({
            el: '#app',
        })
    </script>
{% endblock %}
```

vue 的默认模板语法 `{{ }}` 会和 Jinja2 默认语法冲突, 需要解决该冲突, 否则最终会以 Jinja2 渲染结果为准

1. 用 Jinja2 的 row 语法块跳过后端渲染

   ```html
   {% raw %}
    <div id="app">
        {{ vue_var }}
    </div>
   {% endraw %}
   ```

   这种方式简单无副作用, 只需把使用 vue 语法的地方放入 raw 代码块, 缺点是代码内会多了很多 raw 标记, 可读性较差

2. 修改 Jinja2 的模板语法

    ```python
    from flask import Flask

    app = Flask(__name__)

    app.jinja_env.block_start_string = '(%' # 修改块开始符号
    app.jinja_env.block_end_string = '%)' # 修改块结束符号
    app.jinja_env.variable_start_string = '((' # 修改变量开始符号
    app.jinja_env.variable_end_string = '))' # 修改变量结束符号
    app.jinja_env.comment_start_string = '(#' # 修改注释开始符号
    app.jinja_env.comment_end_string = '#)' # 修改注释结束符号
    ```

3. 修改 vue 的模板语法
   
    ```js
    var app = new Vue({
        el: "#app",
        delimiters: ["${", "}"],
    })
    ```


由于修改 Jinja2 的模板语法是全局生效的, 而我只有部分模板需要引入 vue, 所以最终选择在需要的地方修改 vue 的模板语法.

效果如下: 

```html
<div id="app">
    {% if model %}
        <span>{{ jinja_value }}</span>
    {% end if %}
    <span v-if="model">${vue_value}</span>
</div>
```


## Notes

1. js 中使用 Jinja2 模板时, 需要注意 js 语法规范
    ```js
    // value = Hello Jinja2
    // 作为字符串时需要加上引号
    var foo = '{{ value }}'

    // value1 = '{"a" : 1}'
    // 字符串带双引号(或其他 html 语法的特殊符号)时双引号会被转义, 此时需要加上 safe 标记防止转义
    var foo1 = '{{ value|safe }}
    ```

待续...
