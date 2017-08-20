#!/usr/bin/env python3
# -*- coding: utf-8 -*-




import time, datetime
import tushare 	as ts
import pandas 	as pd
from tqdm import tqdm, trange

import db
import function as fn


def fetch_hist_data():

	rs = db.fetchcol("SELECT code FROM ts_basics")

	pbar = tqdm(rs)
	for char in pbar:
		pbar.set_description("Processing %s" % char)
		time.sleep(0.01)






if __name__ == '__main__':

	fetch_hist_data()
