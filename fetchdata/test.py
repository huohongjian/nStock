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



def test_fetch(code='600300'):
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


def test_k_data(code='600300'):
	starttime = datetime.datetime.now()
	ts.get_h_data(code, start='2017-08-15')
	endtime = datetime.datetime.now()
	print('[ts.get_k_data(code="%s")] fetching   a day data! time=[%s]'%(code, endtime-starttime))

	starttime = datetime.datetime.now()
	ts.get_h_data(code)
	endtime = datetime.datetime.now()
	print('[ts.get_k_data(code="%s")] fetching all day data! time=[%s]'%(code, endtime-starttime))



if __name__ == '__main__':
	test_k_data()