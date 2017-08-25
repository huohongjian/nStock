#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# from tqdm import tqdm, trange
# from time import sleep

from ..libs import db
sql = "SELECT * FROM st_basics LIMIT 2"

rs = db.fetchall(sql)

print(rs)

