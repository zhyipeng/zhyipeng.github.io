> 本来嫌麻烦不想弄 HTTPS 的, 但是搞了个 gitbook 结果 gitbook.com 只支持 https 的图片链接, 那只能把 OSS 加上 https 了, 然后顺便也把博客也加上吧hhhhhh

## 1. 申请证书

七牛云或者其他很多云厂商都有免费的证书申请服务, 但是七牛云还要填一些公司信息什么的, 作为个人使用来说就不方便了, 所以我是去 [FreeSSL](https://freessl.cn/) 申请的.
免费证书品牌有两家, 一个双域名有效期一年, 一个支持通配符域名有效期三个月, 为了省事就申请了一年的那家, 两个域名一个给到 OSS, 另一个就给博客用吧.

选一键申请, 傻瓜式操作, 没啥好说的了.

## 2. 部署

七牛云那边按文档操作, 也没啥好说的- -
然后博客这边, 主要是 nginx 的配置.

- 一个证书, 一个私钥, 丢到服务器上
```bash
scp hostname_chain.crt server:/etc/ssl/certs
scp hostname_key.key server:/etc/ssl/certs
```

- ssl 配置
其实可以直接写在 nginx conf 里, 不过为了复用, 还是起一个新的配置文件.
```bash
echo "ssl on;\nssl_certificate /etc/ssl/certs/hostname_chain.crt;\nssl_certificate_key /etc/ssl/certs/hostname_key.key;" > /etc/nginx/conf.d/hostname.ssl.inc
```

- listen 443
```bash
{
    listen 443 ssl;
    server_name hostname.com;
    include /etc/nginx/conf.d/hostname.ssl.inc;
    location / {
        ...
    }
}

```

- 转发 http
```bash
{
    listen 80;
    server_name hostname.com;
    return 301 https://$server_name$request_uri;
}
```

done.