#!/usr/bin/env python3
# -*- coding: utf-8 -*-


sql = ''

r = {'code':'600300',	'name': 'wwgf',	'area': 'js',	'industry': 'ok',	'pe': 23}


sql = """INSERT INTO st_info(code, 
name, area, industry)
VALUES ('{0}', '{1}', '{2}', '{3}')
CONFLICT (code) do UPDATE SET
		name 	= '{1}',
		area 	= '{2}',
		industry= '{3}';""".format(r['code'],
			r['name'], r['area'], r['industry'])


print(sql)
