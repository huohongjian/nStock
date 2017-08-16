#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
sys.path.append("../")


from libs import db

def create_tables():
	f = open('__install.sql', encoding="utf-8")
	sql = f.read()
	f.close()

	if db.execute(sql):
		print("init database is ok !")
	else:
		print("some wrong is arised !")




if __name__ == '__main__':
    create_tables()

