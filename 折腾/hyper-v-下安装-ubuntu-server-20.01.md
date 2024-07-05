> 在一次系统更新后，wsl2 又双叒叕挂了。之前尝试过卸载 docker 了，看起来不是 docker 的问题。算了，先放弃了，等 windows 稳定版更新 wsl2 再说，装个虚拟机用着先。windows 下的虚拟机，vm/vb/hyper-v，vm 收费，vb 性能稍差些，系统自带的 hyper-v 就成了最佳选择了，搞起！

## 前言

首先明确需求, 作为开发用的虚拟机由于性能等方面的原因并不打算用 IDE 开发, 而是用 neovim 做编辑器, 也就不需要图形界面了.

先找了一下电脑里有没有现成的镜像:

- ubuntu20-arm
- ubuntu20-amd64-desktop
- debian9

arm 架构的先排除, ubuntu 桌面版好像不能不装桌面环境, pass, 就拿 debian 来试试.

装完发现 debian 的 apt 源有点旧, 软件版本很低很低 (难怪说它的优势是稳定...),
然后折腾了下就把 apt 源搞坏了...懒得研究怎么修了, 还是重新去下个 ubuntu 吧....




## 1. 系统镜像

目标系统是 ubuntu20-server, 官网下肯定慢的, ubuntu-cn 试了下也慢, 那就找一下其他的国内源咯: http://mirrors.melbourne.co.uk/ubuntu-releases/20.04.1/



## 2. 装机

hyper-v 快速创建就很简单了, 不过选镜像那一步必须要等微软服务器返回支持的在线系统版本(吐槽一下产品设计),
然而国内访问微软的服务器确实随缘... 运气不好刚好这一次一直没响应, 就手动创建了...

内存动态分配, 硬盘动态, 模拟4个核心, 网络用 default_switch, 虚拟化技术代数选了一代, 二代看起来像是给 wsl2 用的. 微软官方文档也写的很详细了: https://docs.microsoft.com/zh-cn/virtualization/hyper-v-on-windows/quick-start/create-virtual-machine



配置完进入系统开始安装, 第一遍没配代理, 而是直接用了阿里云的镜像源, 结果安装依赖到一半进行不下去了...估计是阿里云源少了什么东西...



好吧, 删掉重来. 这次就还是用默认源了, 为了解决网络问题必须上代理, 用的宿主机代理, ip 可以在宿主机 ipconfig 里看那个 default_switch, 等了会就安装完成了. 

安装完会要求创建一个账号，创建完 `sudo passwd` 设置 root 账号密码， 就可以启用 root 账号了



## 3. 代理

代理（梯子）是必备的，由于宿主机有代理，就不需要在虚拟机里再安装了，直接配置代理地址就行：

```shell
export http_proxy=http[s]://hostname:port
export https_proxy=http[s]://hostname:port
export all_proxy=sock5://hostname:port
```

个人习惯是配置一组 alias 来开关代理：

```shell
alias set_proxy="export http_proxy=http[s]://hostname:port; export https_proxy=http[s]://hostname:port; export all_proxy=sock5://hostname:port"
alias unset_proxy="export http_proxy=''; export https_proxy=''; export all_proxy=''"
```

这样就要求 hostname 要固定，default_switch 默认是优先用桥接模式，也就是 ip 是动态的。

那就查一下怎么固定 ip 吧。。

vm 中有三种网络模式，桥接/net/专用，对应到 hyper-v 就是 外部/内部/专用。其中 net 模式是可以固定 ip 的。

在 hyper-v 管理器里新建一个内部虚拟网络，然后在 windows 网络适配器管理中找到这个网络，将 ipv4 设置为固定 ip 和子网掩码，比如 192.168.137.1 / 255.255.255.0。

回到 ubuntu 下同样设置成固定 ip。

ubuntu 采用 netplan 作为网络配置管理

```shell
$ vim /etc/netplan/{每台机器不一}.yaml

network:
    ethernets:
        eth0:
            addresses: [192.168.137.2/24]
            gateway4: 192.168.137.1
            dhcp4: true
            optional: true
    version: 2

$ netplan apply
```

这个时候应该已经可以互相 ping 通了。不通的话可能需要配置一下 windows 防火墙。

然后将宿主机所用的网络共享给虚拟网络，虚拟机就可以正常联网了。



## 4. 常用软件

待填坑。。。



## 后记

配置完开发环境，把项目拉下来跑一轮单元测试试下性能。这是个 web 项目，单元测试充斥着大量数据库操作，影响时间的主要因素应该就是磁盘 io 了。

| 机器                                               | 时间/s |
| -------------------------------------------------- | ------ |
| mbp2019 款 i5 16g 256固态                          | 约 360 |
| wls2 (宿主机 i5-8300H 2×8g 512g固态，ubuntu-20.01) | 约 600 |
| hyper-v ubuntu-20.01 （宿主机同上）                | 约 450 |
| 树莓派 4b (内存2g，32g 闪迪 sd 卡)                 | 约 600 |
| 某服务器（配置未知，系统未知，用于 gitlab-CI）     | 约 600 |

wsl2 号称大幅提升的磁盘性能看起来也没充分发挥出固态的优势。相较而言，hyper-v 的表现可以说是很出色了，至少对于我的需求来说比 wsl2 更优秀，动态内存的使用完全可以像 wsl2 那样常驻后台运行而不会影响宿主机性能。

