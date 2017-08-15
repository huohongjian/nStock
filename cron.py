#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj

import time
import fetchdata as fd
from datetime import datetime
from function import base as fb



def main():
    print('executing task ... ')
    filename  = '/home/stock/stock/cron.log'
    sleeptime = 6
    fb.writefile(filename, '\n')
    
    if datetime.today().weekday() == 4:     # 0: monday, 4: firday
        fd.fetch_stock_basics()
        fb.writefile(filename, '[%s] stock basics is fetched!\n' % datetime.now())
        fb.sleep(sleeptime)

    fd.fetch_data_hist()
    fb.writefile(filename, '[%s] all stock hist data is fetched!\n' % datetime.now())
    fb.sleep(sleeptime)
    
    fd.reflesh_data_hist_fq()
    fb.writefile(filename, '[%s] hfq & qfq is computed and saved!\n' % datetime.now())
    fb.sleep(sleeptime)
    
    fd.identify_data_hist_price_wave()
    fb.writefile(filename, '[%s] the price wave on table [data_hist] is indentified!\n' % datetime.now())
    fb.sleep(sleeptime)
    
    fd.reflesh_profit_peaks_botts()
    fb.writefile(filename, '[%s] the peaks and botts and days from newly one on table [profit] is reflesh!\n' % datetime.now())
    fb.sleep(sleeptime)
    
    fd.reflesh_profit_prices()
    fb.writefile(filename, '[%s] the prices on table [profit] is reflesh!\n' % datetime.now())
    
    print('task is executed!')
    





if __name__ == '__main__':
    main()
