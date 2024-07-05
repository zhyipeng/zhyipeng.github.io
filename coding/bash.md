# bash

### awk 求和
```bash
awk '{sum += $1};END {print sum}'
```

### awk 筛选数据
```bash
awk '{if ($1>5) print}'
```

### 查找重复行并输出重复次数
```bash
sort test.txt | uniq -dc
```

### VM挂载共享目录
```bash
sudo mount -t fuse.vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other
```