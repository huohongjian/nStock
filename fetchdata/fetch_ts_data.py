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


def fetch_stock_basics():
#	sys.stdout.write('start fetching stock basic info ...')
	print('Now starting to fetch stock basic info ...')
	df = ts.get_stock_basics()
	df.to_sql('stock_basics', ENGINE, if_exists='replace')
	print('is done!')


'''fetching is very slowly.'''
def fetch_stock_today_all():
	print('Now starting to fetch all stock in today trade ...')
	df = ts.get_today_all()
	df.to_sql('stock_today_all', ENGINE, if_exists='replace')
	print('is done!')






def test_speek(code='600300'):
	starttime = datetime.datetime.now()
	ts.get_k_data(code)
	endtime = datetime.datetime.now()
	print('[ts.get_k_data()] fetching %s stock prices! time=[%s]'%(code, endtime-starttime))
	
	starttime = datetime.datetime.now()
	ts.get_h_data(code)
	endtime = datetime.datetime.now()
	print('[ts.get_h_data()] fetching %s stock prices! time=[%s]'%(code, endtime-starttime))

	starttime = datetime.datetime.now()
	ts.get_hist_data(code)
	endtime = datetime.datetime.now()
	print('[ts.get_hist_data()] fetching %s stock prices! time=[%s]'%(code, endtime-starttime))


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






if __name__ == '__main__':
#	fetch_stock_basics()
#	fetch_stock_today_all()

#	test_speek()
	fetch_hist_data()