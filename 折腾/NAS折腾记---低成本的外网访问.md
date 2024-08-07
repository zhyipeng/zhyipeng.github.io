> 最近入了一台绿联 DH4000, 这个配置配合家庭宽带体验可比我那台 2h2g 的小水管服务器好多了. 成品 nas 的好处在于厂商提供云服务, 使我在外网环境也能访问到 nas 上的资源, 除了自部署的服务.

要访问自己部署的服务, 要么要有公网 ip, 要么内网穿透.

# 低成本的外网访问

最近入了一台绿联 DH4000, 这个配置配合家庭宽带体验可比我那台 2h2g 的小水管服务器好多了. 成品 nas 的好处在于厂商提供云服务, 使我在外网环境也能访问到 nas 上的资源, 除了自部署的服务.

要访问自己部署的服务, 要么要有公网 ip, 要么内网穿透.

> 我的场景: nas, 一台短有效期云服务器, 一个长有效期域名, 移动宽带

## 一、公网ip的获取

现如今家庭宽带已经很难获得公网的 ipv4 了, 不过在网上了解到移动宽带是自带 ipv6 的, 只需要开起来就行了. 方法不止一种, 我用的是桥接, 具体参考 [获取移动公网IPV6（光猫桥接）
](https://blog.csdn.net/qq_45060540/article/details/130305363)

设置好之后, 就可以在 nas 网络状态页面看到 ipv6 地址了, 使用 5G 网络访问 `http://[ipv6]:9999` 成功访问到 nas 登录页 (ipv6地址需要中括号括起来才能在浏览器上使用)


## 二、DDNS

> 动态 DNS（DDNS）是一项在 IP 地址发生变化时可以自动更新 DNS 记录的服务

各大域名商都有提供 DDNS 服务, 只需要定时调用其 API 即可.

可以自己写脚本, 也可以用现成的轮子

这里用的是开源的 [ddns-go](https://github.com/jeessy2/ddns-go), 通过 docker 部署在 nas 上

ddns-go 提供常见的 dns 服务商的 API 调用, 只需要配置好参数就可以无脑跑起来了. 并且 ip 获取方式也有多种, 经试验我这里使用 host 网络模式部署的 ddns-go 容器通过网卡获取 ipv6 最稳定直接.

我这里是简单地将 `*.yunshu.fun` 解析到了 ipv6 上

完成后已经可以使用 5G 网络通过域名访问到 nas 上的服务了

## 三、非 ipv6 环境下的外网访问

公司的网络不支持 ipv6, 经过调研大概有三种方式可以解决这个问题:

- 内网穿透
- CDN 套壳
- P2P
- 内网浏览器 - 在 nas 上部署一个内网浏览器, 只要想办法将内网浏览器开放出去, 就可以通过它访问内网的其他服务. 

内网浏览器虽然不算个正经解决办法, 但是对于偶尔需要访问不想暴露在公网的内网服务来说还是有使用场景的

内网穿透无非就是通过具有公网ip的服务器, 第三方(如花生壳)提供的服务器, 通过 ssh 隧道等方式将内网服务代理到公网 ip 的某个端口, 这种方式同时受限于服务器带宽和家庭带宽(上行速率, 后不再赘述), 反正免费或低成本的方案都体验不佳就是了

P2P 或者类似的组网方式, 需要在内网上部署并且稳定运行一个服务端, 速度取决于家庭带宽, 相对没那么稳定吧.

CDN 套壳这种方式完全是因为有 Cloudflare 这个~~慈善机构~~(大误). CF 提供个人免费的 CDN 服务, 并且支持 4to6, 也就是说在没有 ipv6 的网络下访问纯 ipv6 的服务时, 它会给你代理到一个 ipv4 上. 唯一的缺点可能就是国内访问可能多一些延迟, 几十到几百毫秒吧, 问题不大. 相对来说优点一大堆:
- 隐藏服务器真实 ip
- 提供长效的 https 证书
- 免费的防火墙、DDOS防护等
- CDN缓存
- 流量分析等
- ...

要使用 CF, 首先要将域名的 DNS 服务器迁移过来给 CF 管理. 注册好 CF 账号并确认要管理的域名后 CF 会给出 DNS 服务器地址, 到域名商管理页设置就可以了, 可能需要几个小时的生效时间. 迁移时 CF 会扫描原 DNS 服务商的规则, 可以帮你一键迁移过来.

> 参考教程: [开启 Cloudflare CDN 代理，实现 IPv4 to IPv6 转换
](https://blog.csdn.net/qq_38894585/article/details/131054885)

DNS 服务器生效后在非 ipv6 网络下 ping 域名, 已经是 CF 的 ipv4 地址了.

DNS 服务器迁移之后可能会有几个问题:

- 一键迁移的泛解析不生效, 也就是 `*.yunshu.fun` 这条规则, 需要手动编辑一下, 重新填入完整的 `*.yunshu.fun`, 而不只是 `*`
- 端口, CF 支持转发的端口存在限制: 
    - HTTP: 80,8080,8880,2052,2082,2086,2095
    - HTTPS: 443,2053,2083,2087,2096,8443
    > ps: 家用宽带屏蔽了 80/443 端口
    > pps(240711): 突然发现移动 ipv6 没屏蔽 443!
    
    因此对外服务的端口只能使用这些
- HTTPS 证书问题, 我在服务器/nas上是使用 Caddy 来管理 HTTPS 证书的, 属于是将证书放在了服务器, 因此需要在 CF 上将 SSL/TLS 加密模式改为`完全(严格)`
- CF 的免费 CDN 仅支持 HTTP 协议, 例如我将主域名解析到我的云服务器上了, 要使用 ssh 的话就需要取消 CF 的 CDN 代理, 而一旦取消了 CDN 代理, 就无法做 ipv4to6 了. 因此如果需要内网 ssh 的话还是需要走内网穿透等渠道的

经过上述折腾, 已经可以通过诸如 [https://memo.yunshu.fun:8443](https://memo.yunshu.fun:8443) 这样的链接来访问我 nas 上部署的服务了. 

但是在手机等设备上要输入端口号还怪麻烦的, 下一节将用一个简单的方式去掉端口号, 但只限于 HTTP GET 请求, 其他请求还需要探索其他方式

## 四、请求转发

对于 HTTP GET 请求, 最简单的方式就是利用 HTTP Redirect, 将特定的地址重定向到指定地址. 

我选择以一个固定的二级域名为入口, 通过不同的 path 分发到不同的服务.

首先将 `nas.yunshu.fun` 解析到云服务器上, 然后利用 nginx/caddy 返回重定向响应.

以 caddy 为例:

```yaml
nas.yunshu.fun {
        handle /memo {
                redir https://memo.yunshu.fun:8443
        }
        handle /git {
                redir https://git.yunshu.fun:8443
        }
        handle / {
                redir https://n.yunshu.fun:8443
        }
        ...
}
```

这样就可以在浏览器上通过 `https://nas.yunshu.fun/memo` 来访问 nas 上的 memo 了.

对于其他 HTTP 请求, 可以考虑手写一个代理服务来处理, 我这暂时没有使用场景, 就没弄了.
