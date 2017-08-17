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


##################################################################################
def is_trade_day(date):
	r = db.fetchone("SELECT isopen FROM ts_trade_cal WHERE calendar='%s'" % date)
	return True if r[0]==1 else False

def pre_trade_day(date):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar<'%s' AND isopen=1 ORDER BY calendar DESC" % date)
	return datetime.datetime.strptime(r[0], "%Y-%m-%d").date()

def next_trade_day(date):
	r = db.fetchone("SELECT calendar FROM ts_trade_cal WHERE calendar>'%s' AND isopen=1 ORDER BY calendar" % date)
	return datetime.datetime.strptime(r[0], "%Y-%m-%d").date()
	
###################################################################################



# need to fetch once per year.
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


def _get_basics():
#	sys.stdout.write('start fetching stock basic info ...')
	print('Now starting to fetch stock basic info ...')
	df = ts.get_stock_basics()
	df.to_sql('stock_basics', ENGINE, if_exists='replace')
	print('is done!')



def fetch_today_all():
	
	r = db.fetchone("SELECT dtime FROM log WHERE dowork='fetch_today_all' ORDER BY dtime DESC")
	
	fetched = r[0] if r else datetime.datetime(2016,1,1)
	fetchedDay = fetched.date()
	now = datetime.datetime.now()
	today = now.date()

	if (fetchedDay == today):
		if (fetched.time() < datetime.time(15, 30, 0)):
			sql = '''DELETE FROM ts_k_data WHERE date="%s"''' % today
			SQL =  sql + '''; INSERT INTO log (dowork, func, statement) VALUES ('delete data', 'fetch_today_all()', '%s')''' % sql
			db.execute(SQL)
			print('execute statement sucess: %s' % sql)
			_get_today_all();
	else :
		nextTradeDay = next_trade_day(fetchedDay)
		if ( nextTradeDay == today):
			_get_today_all()
		else:
			_get_hist_data(start=nextTradeDay)

	return




def _get_today_all():
	print('Fetch data need about 30s. Please wait a moment...')
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
	db.execute("INSERT INTO log(dowork, statement) VALUES('fetch_today_all', '_get_today_all()')")
	endtime = datetime.datetime.now()
	print('is done! time=[%s]' % (endtime-starttime))



def _get_hist_data(cs=['600300', '300347'], start=''):
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




def _get_k_data(codes=['600300', '300347', '300002', '002247', '000881'], start='2016-01-01'):
	rs = db.fetchall("SELECT code FROM stock_basics limit 100")
	
	codes = [r[0] for r in rs]
	

	
	
	starttime = datetime.datetime.now()
	sql = 'INSERT INTO ts_k_data (code, open, close) VALUES '
	i, s = 0, len(codes)
	for code in codes:
		i += 1
		df = ts.get_k_data(code, start=start)
		print('[%s] fetch data sucess.   %d/%d   time=[%s]' % (code, i, s, datetime.datetime.now() - starttime))
		
		if not df.empty:
			for index, row in df.iterrows():
				sql += "('%s', %f, %f)," % (row['code'], row['open'], row['close'] )
	
	starttime = datetime.datetime.now()
	sql = sql[0:-1]
	db.execute(sql)
	endtime = datetime.datetime.now()
	print('fetch to database sucess! time=[%s]'%( endtime-starttime))
	return

	if df.empty:
		endtime = datetime.datetime.now()
		print('[%s] data is newly, not need to fetch! time=[%s]' % (code, endtime-starttime))
	else:
#		df.to_sql('ts_k_data', ENGINE, if_exists='append')
		endtime = datetime.datetime.now()
		print('[%s] fetch to database sucess! time=[%s] rows=%d'%(code, endtime-starttime, df.shape[0]))




if __name__ == '__main__':
#	fetch_ts_trade_cal()
#	fetch_basics()
#	fetch_today_all()
#	_get_basics()
	_get_k_data()
