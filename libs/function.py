#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import tushare 	as ts
import pandas 	as pd
import numpy 	as np

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

	indexname = df.index.name
	SQL = ''

	tqdm.pandas(desc="Structuring SQL!")

	def _save_df(row):
		index = row.name
#	for index, row in df.iterrows():
		if(mode=='insert' or mode=='upsert'):
			sql = "INSERT INTO " + tablename + "(" + indexname
			for col in df.columns:
				sql += ", " + col

			if isinstance(index, (int, float)):
				sql += ") VALUES (" + str(index)
			else:
				sql += ") VALUES ('{}'".format(index)

			for col in df.columns:
				val = row[col]
				if isinstance(val, (int, float)):
					sql += ", " + str(val)
				else:
					sql += ", '" + val + "'"
			sql += ");"


		elif(mode=='update'):
			sql = "UPDATE " + tablename + " SET "

			for col in df.columns:
				val = row[col]
				if isinstance(val, (int, float)):
					sql += "{}={},".format(col, val)
				else:
					sql += "{}='{}',".format(col, val)
			sql = sql[0:-1]

			if isinstance(index, (int, float)):
				sql += "WHERE {}={};".format(indexname, index)
			else:
				sql += "WHERE {}='{};'".format(indexname, index)


		if(mode=='upsert'):
			sql = sql[0:-1] + " ON CONFLICT (" + indexname + ") do UPDATE SET "
			for col in df.columns:
				t = row[col]
				if isinstance(t, (int, float)):
					sql += "{}={},".format(col, t)
				else:
					sql += "{}='{}',".format(col, t)
			sql = sql[0:-1] + ";"

		print(sql)

		tqdm.pandas()
	

	df.progress_apply(_save_df, axis=1)

	return SQL



if __name__ == '__main__':

	pass