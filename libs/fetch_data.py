#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import sys
#sys.path.append('../')


import time, datetime
import tushare 	as ts
import pandas 	as pd

import db
import function as fn
from tqdm import tqdm, trange



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

	print('Saving data to [ts_stock_basics]...')
	st = datetime.datetime.now()
	df.to_sql('ts_basics', db.ENGINE, if_exists='replace')
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
	df.to_sql('ts_today_all', db.ENGINE, if_exists='replace')
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


def fetch_stock_basics_to_st_basics():
	print('Fetching stock basic info...')
	time.clock()
	df = ts.get_stock_basics()
	print('Fetched data sucess! time=[%s]' % (time.clock()))
	fn.save_df(df, 'st_basics');
	fn.write_log(dowork='fetch_stock_basics_to_st_basics')



def fetch_hist_data_to_st_hist_data(codes, start_date='2016-01-01'):
	if codes is None:
		codes = db.fetchcol("SELECT code FROM st_basics")
		if codes is None:
			print('Please input stock stocks.')
			return False

	stime1 = datetime.datetime.now()
	last_code = codes[-1]
	DF = pd.DataFrame()
	pbar = tqdm(codes)
	for code in pbar:
		stime = datetime.datetime.now()
		fetched_day = db.fetchval("SELECT date FROM st_hist_data WHERE code='{}' ORDER BY date DESC LIMIT 1".format(code))
		if fetched_day is not None:
			start_date = str(fn.next_trade_day(fetched_day))
		
		df = ts.get_hist_data(code, start=start_date)
		pbar.set_description("Fetching data [{}]. Time={}".format(code, datetime.datetime.now()-stime))
		
		if not df.empty:
			df['code'] = code
			DF = pd.concat([DF, df])

		if(DF.shape[0]>5000 or code==last_code):
			print('Saving cached data...', end='\r')		
			DF.to_sql('st_hist_data', db.ENGINE, if_exists='append')
			DF = pd.DataFrame()
			print('Saving cached data... is done!')
			if(code==last_code):
				pbar.set_description('This task is completed! Time={}'.format(datetime.datetime.now()-stime1))
	
	fn.write_log(dowork='fetch_hist_data_to_st_hist_data')	



def addto_st_k_data():
	now   = datetime.datetime.now()
	today = now.date()

	v = db.fetchval("SELECT max(date) FROM st_k_data")
	fetch_day = v if v else datetime.date(2017,8,17)

	if(fetch_day<fn.pre_trade_day(today)):
		_get_k_data(start=str(fn.next_trade_day(fetch_day)))

	elif(fetch_day==fn.pre_trade_day(today)):
		if(now.time()<datetime.time(15, 20, 0)):
			print('Data is newly, today k_data should be fetched after 15:30:00.')
		else:
#				renew_ts_today_all()
				print('Copy data from [ts_today_all] to [st_k_data].')
				db.execute("INSERT INTO st_k_data(date, code, open, close, high, low, volume) \
							SELECT '%s' AS date, code, open, trade, high, low, volume \
							FROM ts_today_all" % (str(today)))
	elif(fetch_day==today):
		print('[st_k_data] data is newly, need no any work.')
	else:
		print('Fetched day more than today, [st_k_data] maybe has some wrong...')


	

def _get_k_data(codes=[], start='2016-01-01', autype='qfq'):
	SQL = 'INSERT INTO st_k_data (date, code, open, close, high, low, volume) VALUES '
	sql = SQL
	if codes==[]:
		codes =  db.fetchcol("SELECT code FROM ts_basics limit 30")
	
	i, s, I	= 0, len(codes), 0
	for code in codes:
		i += 1
		df = ts.get_k_data(code=code, start=start, autype=autype)
		if df.empty:
			print('%d/%d [%s] No data fetched. time=%s' % (i, s, code, time.clock()))
			continue
		else:
			print('%d/%d [%s] Fetched data sucess! time=%s' % (i, s, code, time.clock()))
			for index, r in df.iterrows():
				I += 1
				sql += "('%s', '%s', %f, %f, %f, %f, %f)," % \
				(r['date'], r['code'], r['open'], r['close'], r['high'], r['low'], r['volume'])

		if(I>9999 or i>=s):
			print('Saving data to [st_k_data], please wait a moment...')
			db.execute(sql[0:-1])
			print('Saved data sucess! time=%s'%(time.clock()))
			sql = SQL
			I 	= 0
	return True



if __name__ == '__main__':

#	renew_ts_trade_cal()

#	_get_k_data()
	
#	addto_st_k_data()

#	renew_ts_today_all()

#	fetch_stock_basics_to_st_basics()

	fetch_hist_data_to_st_hist_data()
