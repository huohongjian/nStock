#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj

from datetime         import datetime
from Class.XuanGu     import XuanGu
from Class.StockInfo  import StockInfo
from Class.GreyExpect import GreyExpect


def main(code='600300'):
    xg = XuanGu([code])
    si = StockInfo(code)
    ge = GreyExpect()
    
    while True:
        starttime = datetime.now()
        xg.show_info()
        
        print('[recent price]:')
        si.code = code
        si.display_info()
        
        print('\n[Grey Expect]:')
        ge.main(code)
        
        endtime = datetime.now()
        print '[%ss]' % str((datetime.now() - starttime))[-9:-4],
        i  = raw_input('please input stock code:').lower()
        if i in ['m', 'menu', 'h', 'help', '?']:
            pass
        elif i in ['e', 'x', 'exit']: break
        elif len(i) == 6:
            xg._cs = [i]
            code = i


if __name__ == '__main__':
    main()



