#!/usr/bin/env python


#!/usr/bin/env python
#import sys
#sys.path.append("../Class")


from Postgresql import Postgresql as PS
import getinfo as gi

def create_tables():
    ps = PS()
    f = open('__install.sql', encoding="utf-8")
    sql = f.read()
    if ps.execute(sql):
        print("init database is ok !")
    else:
        print("some wrong is arised !")

    f.close();

'''
def init_table_stock_fetch_log():
    ''init table stock_fetch_log''
    codes = gi.get_codes(fields=['al'])
    ps = PS()
    sql = ''
    for c in codes:
        date = gi.get_newly_date(c)
        sql = "INSERT INTO stock_fetch_log (code, newlydate) VALUES ('%s', '%s');" % (c, date)
        ps.execute(sql)
        print("[ %s ] init table stock_fetch_log is ok !" % c)
'''

if __name__ == '__main__':
    create_tables()

