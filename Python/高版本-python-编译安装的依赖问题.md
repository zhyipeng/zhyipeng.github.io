> 以 ubuntu 为例, apt 资源往往跟不上 python 版本的更新, 而且为了稳定性系统往往不会经常更新, 因此编译安装 python 高版本是必要的. 

# 高版本 python 编译安装的依赖问题

以 ubuntu 为例, apt 资源往往跟不上 python 版本的更新, 而且为了稳定性系统往往不会经常更新, 因此编译安装 python 高版本是必要的. 
然而编译安装会遇到不少坑...

## 1. 依赖
### lib 依赖

| 依赖的python/c模块 | 对应的 python 库 | apt包 | yum包 |
| -- | -- | -- | -- |
| _ctype | 很多, 如fire | libffi-dev | libffi-devel |
| bz2 | pandas | libbz2-dev | bzip2-devel |
| _sqlite3 | sqlite3 | libsqlite3-dev | sqlite-devel |

> 持续迭代

### openssl

Python3.10 及以上版本要求 openssl 版本 >= 1.1.1

```bash
find /etc/ -name openssl.cnf -printf "%h\n"
# /etc/ssl

curl -O https://www.openssl.org/source/openssl-VERSION.tar.gz
tar xzf openssl-VERSION
pushd openssl-VERSION
./config \
    --prefix=/usr/local/openssl1.1.1 \
    --libdir=lib \
    --openssldir=/etc/ssl
make -j1 depend
make -j8
make install_sw
popd
```

在编译时需要指定 openssl 目录:

```bash
./configure -C --with-openssl=/usr/local/openssl1.1.1 --with-openssl-rpath=auto --prefix=/usr/local/python3.10
make -j8
make altinstall
```
