#!/usr/bin/env python

import psycopg2


conn = False
try:
	conn = psycopg2.connect(
		database= 'stock',
		host	= 'localhost',
		port 	= '5432',
		user 	= 'postgres',
		password= ''
	)
except Exception as e:
	print("connect database failed, %s" % e)



def fetchall(sql):
	if(conn):
		try:
			cursor = conn.cursor()
			cursor.execute(sql)
			res = cursor.fetchall()
			return res
		except Exception as e:
			print("fetchall exception: %s" % e)
			return False
	print("connect database failed.")
	return False


def fetchone(sql):
	if(conn):
		try:
			cursor = conn.cursor()
			cursor.execute(sql)
			res = cursor.fetchone()
			return res
		except Exception as e:
			print("fetchone exception: %s" % e)
			return False
	print("connect database failed.")
	return False


def execute(sql, returning=False):
	if(conn):
		try:
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			return True
		except Exception as e:
			print("execute exception: %s" % e)
			return False
	print("connect database failed.")
	return False



'''

import psycopg2
from sqlalchemy import create_engine
DBHOST = 'localhost'
DBPORT = '5432'
DBNAME = 'stock'
DBUSER = 'postgres'
DBPASSWORD = ''
DBCHARSET = 'UFT-8'


class Sqlalchemy:
    def __int__(self):
        pass

    def create_engine(self):
        engine = False
        try:
            engine = create_engine('postgresql://%s:%s@%s/%s' % (DBUSER, DBPASSWORD, DBHOST, DBNAME), echo=False)
        except Exception as data:
            print("connect database failed, %s" % data)
            engine = False
        return engine



class Postgresql:
    def __init__(self, dbname=None, dbhost=None):
        if dbname is None:
            self._dbname = DBNAME
        else:
            self._dbname = dbname
        if dbhost is None:
            self._dbhost = DBHOST
        else:
            self._dbhost = dbhost
        
        self._dbport = int(DBPORT)
        self._dbuser = DBUSER
        self._dbpassword = DBPASSWORD
        self._dbcharset = DBCHARSET
        self._conn = self.connect()
        
        if(self._conn):
            self._cursor = self._conn.cursor()


    def __del__(self):
        self.close()


    def connect(self):
        conn = False
        try:
            conn = psycopg2.connect(database=self._dbname,
                    host=self._dbhost,
                    port=self._dbport,
                    user=self._dbuser,
                    password=self._dbpassword
                    )
        except Exception as data:
            print("connect database failed, %s" % data)
            conn = False
        return conn


    def fetchall(self, sql):
        res = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception as data:
                res = False
                print("query database exception, %s" % data)
        return res


    def fetchone(self, sql):
        res = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchone()
            except Exception as data:
                res = False
                print("query database exception, %s" % data)
        return res


    def fetchfield(self, sql, i=0):
        res = self.fetchall(sql)
        if res is None:
            return []
        else:
            return [r[i] for r in res]


    def execute(self, sql, returning=False):
        if(self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                if returning:
                    self._cursor.fetchall()
                else:
                    return True
            except Exception as data:
                print("update database exception, %s" % data)
                return False


    def update_insert(self, table=None, where=None, **ps):
        if table is None or where is None:
            print("please confirm table name or where!")
            return False
        
        update_set = insert_key = insert_val = ''
        for k, v in ps.items():
            insert_key += "%s, " % k
            if isinstance(v, str):
                update_set += "%s='%s', " % (k, v)
                insert_val += "'%s', " % v
            else:
                update_set += "%s=%s, " % (k, v)
                insert_val += "%s, " % v
        update_set = update_set[:-2]
        insert_val = insert_val[:-2]
        insert_key = insert_key[:-2]
            
        sql = "SELECT * FROM %s WHERE %s;" % (table, where)
        r = self.fetchone(sql)
        if r:
            sql = "UPDATE %s SET %s WHERE %s;" % (table, update_set, where)
        else:
            sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, insert_key, insert_val)
        # print sql
        self.execute(sql)
        return True
    

    def close(self):
        if(self._conn):
            try:
                if(type(self._cursor)=='object'):
                    self._cursor.close()
                if(type(self._conn)=='object'):
                    self._conn.close()
            except Exception as data:
                print("close database exception, %s,%s,%s" % (data, type(self._cursor), type(self._conn)))
        return True




'''
