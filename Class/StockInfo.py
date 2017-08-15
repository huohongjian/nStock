#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj

from datetime   import datetime
from Postgresql import Postgresql


class StockInfo:
    def __init__(self, code=None):
        self.code  = code if code is not None else '600300'
        self.ps    = Postgresql()
        self.limit = 5
    
    def main(self):
        print('[recent price]:')
        self.display_info()
                
                
    def display_info(self):
        sql = "SELECT date, close, price_change, p_change, volume, turnover, qfq FROM data_hist WHERE code='%s' ORDER BY date DESC LIMIT %d;" % (self.code, self.limit)
        rs  = self.ps.fetchall(sql)
        if rs is None: return
        print('    date      close     pc      pcr    volume   turnover')
        for r in rs:
            print(' %s %7.2f %7.2f %7.2f%% %9s %7.2f%%' % (r[0], r[1]*r[6], r[2], r[3], format(int(r[4]), ','), r[5]))
        
        
        
        


if __name__ == '__main__':
    si = StockInfo()
    si.main()