#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import tushare as ts
import pandas as pd

import db


def write_log(dowork='', remark=''):
	sql = "INSERT INTO st_log (dowork, remark) VALUES ('%s', '%s')" % (dowork, remark)
	return db.execute(sql)


def is_trade_day(date):
	r = db.fetchone("SELECT isopen FROM ts_trade_cal WHERE calendar='%s'" % date)
	return True if r[0]==1 else False

def pre_trade_day(date, n=1):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar<='%s' AND isopen=1 ORDER BY calendar DESC OFFSET %d LIMIT 1" % (date, n))
	return datetime.datetime.strptime(r[0], "%Y-%m-%d").date()

def next_trade_day(date, n=1):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar>='%s' AND isopen=1 ORDER BY calendar ASC OFFSET %d LIMIT 1" % (date, n))
	return datetime.datetime.strptime(r[0], "%Y-%m-%d").date()




if __name__ == '__main__':

	pass