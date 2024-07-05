> Django orm 非常好用, 然而使用的过程中也发现一些坑, 在这里记录下...

本文基于 django 2.22

1. get_or_create 不是并发安全的, 高并发下容易产生多条一模一样的数据, 后续再次查询时就会产生 MultipleObjectsReturned 异常
2. update_or_create 加了事务锁, 相对 get_or_create 要好些, 但是不支持 update_fields, 因此在某些场景下有会并发写入的问题
> This method is atomic assuming that the database enforces uniqueness of the keyword arguments (see unique or unique_together). If the fields used in the keyword arguments do not have a uniqueness constraint, concurrent calls to this method may result in multiple rows with the same parameters being inserted.
