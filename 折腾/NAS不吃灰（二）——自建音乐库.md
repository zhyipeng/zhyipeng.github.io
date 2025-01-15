> 我的音乐需求主要是在 Android 车机上，偶尔也会用其他平台（mac，win，Android 手机）听歌，所以全平台是刚需了。本来是一直用 QQ 音乐年费的，pdd 八十多一年也不贵，曲库也全，车机上开边听边存功能也不怎么耗流量。但是某天车机播放时突然中断了，发现歌单里的歌变灰了，说没版权了。emmmmm，还是考虑自建音乐库吧

## 音源
由于版权问题，现在互联网上不太好找到齐全的曲库，从主流音乐平台获取资源反而是最简单的了。目前我的 QQ 音乐会员还在，所以就直接从 QQ 音乐下载音源了，等过期后再考虑其他的
- QQ 音乐（需要会员）以及格式转换工具
- 酷我音乐魔改版
- BiliBili/Youtube，音源质量不保证
- 网盘，搜索困难，不集中

### 格式转换
各家音乐平台的 vip 歌曲基本都是用的私有格式，需要使用一些[工具](https://github.com/ipid/unlock-music) 转为通用的音乐格式。
> 由于不可描述的原因，建议多备份此工具，该项目原仓库就被 DMCA 了

### 音乐标签
被格式转换后会丢失一些信息，可以使用 [音乐标签web版](https://github.com/xhongc/music-tag-web) 来编辑

## 存储和分发
目前曲库也就十来个 G，就优先考虑本地播放了，需要将各个设备与 nas 之间进行同步。windows/mac 端绿联软件直接支持了文件同步的功能，但不知道为啥移动端没有这个功能，所以还是需要找第三方的工具 [syncthing](https://github.com/syncthing/syncthing)

nas 端使用 [docker 镜像](https://hub.docker.com/r/syncthing/syncthing) 运行 syncthing，把曲库挂载进去就行了
安卓端使用官方提供的 [app](https://github.com/syncthing/syncthing-android)

> 安卓端原生功能严重残缺，很多操作都需要到 web 界面进行

## 播放器
之前购买过 poweramp，所以手机和车机都用这个了，备选 [椒盐音乐](https://github.com/Moriafly/SaltPlayerSource) （闭源）

pc 端 [dopamine](https://github.com/digimezzo/dopamine-windows)，c# 写的，作者正在使用 electron 重构 3.0 版本以支持跨平台

mac 端还在找，dopamine3.0 可以期待一下