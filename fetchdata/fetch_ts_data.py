#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')


import time, datetime
import tushare as ts
import pandas as pd

from libs import db



from sqlalchemy import create_engine
DBHOST = '127.0.0.1'
DBPORT = '5432'
DBNAME = 'stock'
DBUSER = 'postgres'
DBPASSWORD = ''
DBCHARSET = 'UFT-8'

ENGINE = create_engine('postgresql://%s:%s@%s/%s' % (DBUSER, DBPASSWORD, DBHOST, DBNAME), echo=False)


# only need to fetch once per year.
def fetch_ts_trade_cal():
	starttime = datetime.datetime.now()
	print('Fetching trade calender ...')
	df = ts.trade_cal()
	print('Fetched data sucess! And Starting save data to database ...')
	df.rename(columns = {
		'calendarDate'	: 'calendar', 
		'isOpen'		: 'isopen'
	}, inplace=True)
	df = df.set_index('calendar')
	df.to_sql('ts_trade_cal', ENGINE, if_exists='replace')
	endtime = datetime.datetime.now()
	print('Saved to database sucess! time=[%s]' % (endtime-starttime))


def fetch_stock_basics():
#	sys.stdout.write('start fetching stock basic info ...')
	print('Now starting to fetch stock basic info ...')
	df = ts.get_stock_basics()
	df.to_sql('stock_basics', ENGINE, if_exists='replace')
	print('is done!')


'''fetching time is 30's.'''
def fetch_stock_today_all():
	today = datetime.date.today()
	r = db.fetchone("SELECT dtime FROM fetch_data_log WHERE dowork='fetch_today_all' ORDER BY dtime DESC")
	if r[0]:
		print(r[0]>today)
		print(today)


	return

	starttime = datetime.datetime.now()
	df = ts.get_today_all()
	endtime = datetime.datetime.now()
	print('\nFetching data is done! time=[%s]' % (endtime-starttime))

#   df.columns = ['code', name', 'changepercent', 'trade', 'open', 'high', 'low', 'settlement'
#				'volume', 'turnoverratio', 'amount', 'per', 'pb', 'mktcap', 'nmc']	
	print('Processing data ... ')
	df.drop(['name', 'per', 'pb', 'mktcap', 'nmc'], axis=1, inplace=True)
	df.rename(columns = {
		'changepercent'	: 'percent', 
		'trade'			: 'close',
		'settlement'	: 'settle',
		'turnoverratio'	: 'ratio',
		}, inplace=True)
	today = str(datetime.date.today())
	df['date'] = today
	df = df.set_index('date')

	print('Starting save data to database ... ')

	starttime = datetime.datetime.now()
	df.to_sql('ts_k_data', ENGINE, if_exists='append')
	db.execute("INSERT INTO log(dowork, status) VALUES('fetch_today_all', True)")
	endtime = datetime.datetime.now()
	print('is done! time=[%s]' % (endtime-starttime))



def fetch_hist_data(cs=['600300', '300347']):
	today = datetime.date.today()
	weekday = today.weekday()
	if weekday==5:
		today -= datetime.timedelta(days=1)
	elif weekday==6:
		today -= datetime.timedelta(days=2)

#	cs = getinfo.get_codes(fields=['tradable'])
	i, s = 0, len(cs)
	
	for c in cs:
		starttime = datetime.datetime.now()
		i += 1
		r = db.fetchone("SELECT * FROM ts_hist_data WHERE code='%s'" % c)

		if r[0]:
			date = r[0] + datetime.timedelta(days=1)
			if date > today: 
				print('[%d/%d=%.1f%%] %s price is newly!'%(i, s, float(i)/float(s)*100, c))
				continue
			try:
				df = ts.get_hist_data(c, start=str(date))
			except Exception as data:
				df = None
				print(data)

			if df is None: 
				print('[%d/%d=%.1f%%] %s price is newly!'%(i, s, float(i)/float(s)*100, c))
				continue 
		else:
			try:
				df = ts.get_hist_data(c)
			except Exception as data:
				print(data)
		df.insert(0, 'code', pd.Series([c], index=df.index))
		df.to_sql('ts_hist_data', ENGINE, if_exists='append')
		
		endtime = datetime.datetime.now()
		print('[%d/%d=%.1f%%] fetching %s stock prices! time=[%s]'%(i, s, float(i)/float(s)*100, c, endtime-starttime))

	print('stock histroy prices is fetched!')




def fetch_k_data(code='600300', start='2016-01-01'):
	starttime = datetime.datetime.now()
	r = db.fetchone("SELECT max(date) FROM ts_k_data WHERE code='%s'" % code)
	if r[0]:
		start = str(r[0] + datetime.timedelta(days=1))

	df = ts.get_k_data(code, start=start).set_index('date')

	if df.empty:
		endtime = datetime.datetime.now()
		print('[%s] data is newly, not need to fetch! time=[%s]' % (code, endtime-starttime))
	else:
#		df.to_sql('ts_k_data', ENGINE, if_exists='append')
		endtime = datetime.datetime.now()
		print('[%s] fetch to database sucess! time=[%s] rows=%d'%(code, endtime-starttime, df.shape[0]))


def exe_fetch_k_data():
	cs = ['600300', '300347', '300002', '002247', '000881']
	for code in cs:
		fetch_k_data(code)


if __name__ == '__main__':
#	fetch_stock_basics()
#	fetch_stock_today_all()

#	exe_fetch_k_data()
	fetch_ts_trade_cal()