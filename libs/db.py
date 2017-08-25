#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from sqlalchemy import create_engine

DBHOST = '127.0.0.1'
DBPORT = '5432'
DBNAME = 'stock'
DBUSER = 'postgres'
DBPASSWORD = ''
DBCHARSET = 'UFT-8'


ENGINE = create_engine('postgresql://%s:%s@%s/%s' % (DBUSER, DBPASSWORD, DBHOST, DBNAME), echo=False)





def conn():
	try:
		conn = psycopg2.connect(
			database= 'stock',
			host	= 'localhost',
			port 	= '5432',
			user 	= 'postgres',
			password= ''
		)
	except Exception as e:
		conn = False
		print("connect database failed, %s" % e)
	return conn

CONN = conn()


def fetchall(sql):
	if(CONN):
		try:
			cursor = CONN.cursor()
			cursor.execute(sql)
			res = cursor.fetchall()
			return res
		except Exception as e:
			print("fetchall exception: %s" % e)
			return False
	print("connect database failed.")
	return False


def fetchone(sql):
	if(CONN):
		try:
			cursor = CONN.cursor()
			cursor.execute(sql)
			res = cursor.fetchone()
			return res
		except Exception as e:
			print("fetchone exception: %s" % e)
			return False
	print("connect database failed.")
	return False

def fetchrow(sql):
	return fetchone(sql)

def fetchcol(sql, i=0):
	return [r[i] for r in fetchall(sql)]

def fetchval(sql, i=0):
	r = fetchone(sql)
	return (None,) if r is None else r[i]



def execute(sql, returning=False):
	if(CONN):
		try:
			cursor = CONN.cursor()
			cursor.execute(sql)
			CONN.commit()
			return True
		except Exception as e:
			print("execute exception: %s" % e)
			return False
	print("connect database failed.")
	return False


def close():
	if(CONN):
		try:
			if(type(CONN.cursor)=='object'):
				CONN.cursor.close()
			if(type(CONN)=='object'):
				CONN.close()
		except Exception as e:
			print("close db error: %s" % (e))
			return False
	return True

