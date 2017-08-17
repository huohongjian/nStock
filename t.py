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
	t = datetime.datetime.strptime(r[0], "%Y-%m-%d")
	return datetime.date(t.year, t.month, t.day)

def next_trade_day(date):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar>'%s' AND isopen=1 ORDER BY calendar" % date)
	t = datetime.datetime.strptime(r[0], "%Y-%m-%d")
	return datetime.date(t.year, t.month, t.day)




r = db.fetchone("SELECT dtime FROM fetch_data_log WHERE dowork='fetch_today_all' ORDER BY dtime DESC")
t = next_trade_day(r[0])



today = datetime.date.today()
nday = today + datetime.timedelta(days=1)

print(nday.year)


print(t, nday)
print(t == nday)