#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import sys
#sys.path.append('../')


import time, datetime
import tushare 	as ts
import pandas 	as pd

import db
import function as fn




# need to fetch once per year.
def renew_ts_trade_cal():
	print('Fetching trade calender...')
	st = datetime.datetime.now()
	df = ts.trade_cal()
	print('Fetched data sucess! time=[%s]' % (datetime.datetime.now()-st))

	print('Starting save data to [ts_trade_cal]...')
	st = datetime.datetime.now()
	df.rename(columns = {
		'calendarDate'	: 'calendar', 
		'isOpen'		: 'isopen'
	}, inplace=True)
	df = df.set_index('calendar')
	df.to_sql('ts_trade_cal', db.ENGINE, if_exists='replace')
	fn.write_log(dowork='get_ts_trade_cal', remark='ok')
	print('Saved data sucess! time=[%s]\n' % (datetime.datetime.now()-st))
	return True


def renew_ts_basics():
#	sys.stdout.write('start fetching stock basic info ...')
	print('Fetching stock basic info...')
	st = datetime.datetime.now()
	df = ts.get_stock_basics()
	print('Fetched data sucess! time=[%s]' % (datetime.datetime.now()-st))

	print('Saving data to [ts_basics]...')
	st = datetime.datetime.now()
	df.to_sql('ts_basics', ENGINE, if_exists='replace')
	fn.write_log(dowork='get_ts_basics', remark='ok')
	print('Saved data sucess! time=[%s]\n' % (datetime.datetime.now()-st))
	return True


def renew_ts_today_all():
	print('Fetching real-time data of today all tradable stock...')
	st = datetime.datetime.now()
	df = ts.get_today_all()
	print('\nFetched data sucess! time=[%s]' % (datetime.datetime.now()-st))

	print('Saving data to [ts_today_all]...')
	st = datetime.datetime.now()
	df.to_sql('ts_today_all', ENGINE, if_exists='replace')
	fn.write_log(dowork='get_ts_today_all', remark='ok')
	print('Saved data sucess! time=[%s]\n' % (datetime.datetime.now()-st))
	return True

'''
def get_ts_hist_data(codes=[], start='2017-07-01'):
	print('Fetching history data though stock code without autype...')
	st = datetime.datetime.now()
	df = ts.get_hist_data(code)
	print('\nFetched data sucess! time=[%s]' % (datetime.datetime.now()-st))

	print('Saving data to [ts_today_all]...')
	st = datetime.datetime.now()
	df.to_sql('ts_today_all', ENGINE, if_exists='replace')
	fn.write_log(dowork='get_ts_today_all', remark='ok')
	print('Saved data sucess! time=[%s]\n' % (datetime.datetime.now()-st))
	return True
'''




def addto_st_k_data():
	now   = datetime.datetime.now()
	today = now.date()

	r = db.fetchone("SELECT max(date) FROM st_k_data")
	fetch_day = r[0] if r[0] else datetime.date(2016,1,1)


	if(fetch_day<fn.pre_trade_day(today)):
		_get_k_data(start=str(fn.next_trade_day(fetch_day)))
	elif(fetch_day==fn.pre_trade_day(today)):
		if(now.time()<datetime.time(15, 20, 0)):
			print('Please wait to 15:30:00, then start to fetch data.')
		else:
			#_addto_st_k_data_2()

			pass
	elif(fetch_day==today):
		print('The data is newly, need no any work.')
	else:
		print('Fetched day more than today, please check table [st_k_data], maybe has some wrong...')


def _get_k_data(codes=[], start='2016-01-01', autype='qfq'):
	SQL = 'INSERT INTO st_k_data (date, code, open, close, high, low, volume) VALUES '
	sql = SQL
	rs 	= db.fetchall("SELECT code FROM ts_basics limit 30")
	i 	= 0
	s 	= len(rs)
	I 	= 0
	for r in rs:
		st = datetime.datetime.now()
		i += 1
		code = r[0]
		df = ts.get_k_data(code=code, start=start, autype=autype)
		print('%d/%d [%s] Fetched data sucess! time=[%s]' % (i, s, code, datetime.datetime.now()-st))
		
		if not df.empty:
			for index, row in df.iterrows():
				I += 1
				sql += "('%s', '%s', %f, %f, %f, %f, %f)," % \
				(row['date'], row['code'], row['open'], row['close'], row['high'], row['low'], row['volume'])

		if(I>10000):
			_save_data_to_ts_k_data(sql[0:-1])
			sql = SQL
			I 	= 0
	
	if (sql != SQL):
		_save_data_to_ts_k_data(sql[0:-1])
	return True


def _save_data_to_ts_k_data(sql):
	st = datetime.datetime.now()
	print('Now saving data to [ts_k_data], please wait a moment...')
	db.execute(sql)
	print('Saved data sucess! time=[%s]'%(datetime.datetime.now()-st))
	return True


if __name__ == '__main__':

#	renew_ts_trade_cal()

	addto_st_k_data()