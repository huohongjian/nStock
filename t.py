#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, datetime, time
from libs import db





#d1 = datetime.datetime.strptime('2015-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')



def is_trade_day(date):
	r = db.fetchone("SELECT isopen FROM ts_trade_cal WHERE calendar='%s'" % date)
	return True if r[0]==1 else False

def pre_trade_day(date):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar<'%s' AND isopen=1 ORDER BY calendar DESC" % date)
	return datetime.datetime.strptime(r[0], "%Y-%m-%d").date()

def next_trade_day(date):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar>'%s' AND isopen=1 ORDER BY calendar" % date)
	return datetime.datetime.strptime(r[0], "%Y-%m-%d").date()




r = db.fetchone("SELECT dtime FROM log WHERE dowork='fetch_today_all' ORDER BY dtime DESC")
print(r)

t = next_trade_day(r[0])



today = datetime.date.today()
nday = today + datetime.timedelta(days=1)



print(t, nday)
print(t == nday)
