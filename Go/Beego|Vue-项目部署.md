> 目前已经做出了一版有基础文章、分类管理的版本，就先部署一版看看效果

# Beego
编译型语言部署还是比较简单的，build 好丢上服务器跑就行了....


大雾...

数据库、环境变量啥的都不一样，还是推荐在服务器构建，还节省带宽，毕竟 build 出来的可执行文件还是挺大的。

唯一踩到的坑就是装依赖把我那 1H1G 的服务器搞垮了吧。。。原因未知，ssh 都挂了上不去，web 端控制台显示磁盘一直在读数据，
最后重启发现依赖已经装好了。。。

还是列一下步骤吧：

1. 安装 go
```bash
wget https://dl.google.com/go/go1.14.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.14.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

2. 拉代码 略

3. 安装依赖&build
```bash
go build main.go  # build 的时候会自动装依赖
```
> 国内服务器可以加一下七牛代理 `export GOPROXY=https://goproxy.cn`

4. 配置 supervisor
	
    其实就是 Beego 文档那个配置
```bash
[program:mypage-backend]
directory = /srv/www/mypage-backend
command = /srv/www/mypage-backend/main
autostart = true
startsecs = 5
user = root
redirect_stderr = true
stdout_logfile = /etc/supervisor/logs/beego.log
```

5. nginx 代理

	不是必须，beego 可以直接设置监测 TCP 80 端口请求。
    
    配 nginx 可以方便和其他项目共用 80 端口，还有访问日志、负载均衡等等...
```bash
server {
    listen      80;
    server_name zhyipeng.com; 
    charset     utf-8;

    client_max_body_size 75M; 

    location /v1 {
		try_files /_not_exists_ @backend;
    }

    location @backend {
		proxy_set_header X-Forwarded-For $remote_addr;
		proxy_set_header Host            $http_host;

		proxy_pass http://127.0.0.1:8088;
    }
}
```
> 这份也是 beego 文档上的配置稍微改动下


重载 supervisor，重启 nginx，接口已经可以访问了。

# Vue

Vue build 出来就是一份静态文件了，理论上把 dist 目录丢到服务器或托管商就直接可以用了的。。。

## github pages
想直接部署到 github pages，毕竟免费空间+免费流量+免费域名它不香吗？

vue-cli 文档上就有部署到 github pages 的脚本，原理很简单，也就是把 dist push 到一个单独的仓库/分支，然后在 github pages 上配置就完事了。

部署很顺利，主页样式也加载出来了，然而。。。接口访问不到，应该说接口请求压根没发出去，大概查了下应该是 github pages 域名默认是 https 的，
然后不支持域内请求 http 的资源。。。

手上暂时没有其他域名，服务器也没有 https 证书，就这样吧。。。。


## 部署到服务器

丢到服务器某个目录然后 nginx 代理一下就行了，应该没啥要特殊说的了。



----
最后出来的效果看起来还不错，单页应用 + Go 接口页面加载比之前 django 渲染快多了。

