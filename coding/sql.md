# sql

### 查重
```sql
# 查重
select * from user where (nick_name,password) in
     (select nick_name,password from user group by nick_name,password where having count(nick_name)>1);
# 筛选重复记录的最大 id
select * from user where id in
     (select max(id) from user group by nick_name,password where having count(nick_name)>1);
```

### 分组取最值
```sql
select a.*
from (
	select uid, max(created) as c from table1 
	group by uid
) b join table1 a on a.uid=b.uid and a.created = b.c;
```