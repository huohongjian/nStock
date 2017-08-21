#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import tushare 	as ts
import pandas 	as pd
import numpy 		as np

from tqdm import tqdm, trange

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





def save_df(df, tablename, mode='upsert'):
	if df.empty:
		print('This dataframe is empty')
		return False

	SQL = ''
	cache = 5000
	indexname = df.index.name
	lines 			= df.shape[0]
	columns   	= df.columns
	colTypes 	= df.dtypes
	indexType = df.index.dtype
	saveTimes = 0

	bar = trange(lines)
	for i in bar:
		row = df.ix[i]
		index = row.name
		bar.set_description("Structuring SQL [{}]".format(index))
		
		if(mode=='insert' or mode=='upsert'):
			sql = "INSERT INTO " + tablename + "(" + indexname
			for col in df.columns:
				sql += ", " + col
			sql += ") VALUES ("
			if indexType in ('int', 'float'):
				sql += str(index)
			else:
				sql += "'" + str(index) + "'"

			for col in columns:
				if colTypes[col] in ('int', 'float'):
					sql += ", " + str(row[col])
				else:
					sql += ", '" + str(row[col]) + "'"
			sql += ");"

		elif(mode=='update'):
			sql = "UPDATE " + tablename + " SET "
			for col in columns:
				if colTypes[col] in ('int', 'float'):
					sql += "{}={},".format(col, row[col])
				else:
					sql += "{}='{}',".format(col, row[col])
			sql = sql[0:-1] + "WHERE " + indexname + "="

			if indexType in ('int', 'float'):
				sql +=  index + ";"
			else:
				sql += "'" + index + "';"

		if(mode=='upsert'):
			sql = sql[0:-1] + " ON CONFLICT (" + indexname + ") do UPDATE SET "
			for col in df.columns:
				if colTypes[col] in ('int', 'float'):
					sql += "{}={},".format(col, row[col])
				else:
					sql += "{}='{}',".format(col, row[col])
			sql = sql[0:-1] + ";"

		SQL += sql
		if(i%cache==cache-1 or i==lines-1):
			saveTimes += 1
			bar.set_description("Saving cached data [{}].".format(saveTimes))
			db.execute(SQL)
			SQL = ''
		if(i==lines-1):
			bar.set_description("This task is done!")
	return True



if __name__ == '__main__':

	pass
