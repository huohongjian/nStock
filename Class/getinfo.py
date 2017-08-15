#!/usr/bin/env python
#encoding:utf-8
#author:hhj


import datetime
from Postgresql import Postgresql as PS




def get_codes(fields=['al']):
    sql = "SELECT code FROM stock_list ORDER BY code ASC"
    if fields not in  [['al'], [''], []]:
        wh = 'True'
        for f in fields:
            wh += ' AND %s'%f
        sql = "SELECT code FROM stock_list WHERE %s ORDER BY code ASC"%wh
    ps = PS()
    rs = ps.fetchall(sql)
    ps.close()
    return [r[0] for r in rs]


def get_newly_date(code='000001'):
    '''get newly data from data_hist'''
    if code is None or code=='':
        return datetime.date(1975,9,2)
    
    sql = "SELECT max(date) FROM data_hist WHERE code='%s'"%code
    ps = PS()
    r = ps.fetchone(sql)
    date = r[0] if r is not None else datetime.date(1975,9,2)
    ps.close()
    return date



if __name__ == '__main__':
    print(get_codes())