#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import db
import pandas as pd
import numpy  as np


sql = "SELECT * from st_basics LIMIT 2"
df = pd.read_sql(sql, db.ENGINE)

print(df)
