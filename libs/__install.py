#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import db
import fetch_data 	as fd
import function 	as fn

def create_tables():
	f = open('__install.sql', encoding="utf-8")
	sql = f.read()
	f.close()

	if db.execute(sql):
		fn.write_log(dowork='create_tables', remark='ok')
		print("init database is ok!\n")
	else:
		fn.write_log(dowork='create_tables', remark='failed')
		print("some wrong is arised!\n")


def init_data():
	print('Now init data, need fetch data though internet, please wait a moment...')
	fd.get_ts_trade_cal()



if __name__ == '__main__':
    create_tables()
    init_data()

