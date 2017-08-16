#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

print(sys.getdefaultencoding()) 


print('u包含中文的str')


from libs import db

#db.execute("insert into tbl(name, signup) values ('huo', '2017-8-9')")

rs = db.fetchone("select * from stock_basics")

print(rs)


