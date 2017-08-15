#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author    hhj
# date      2015-12-28
# version   1.0

import cron
from Class.XuanGu     import XuanGu
from Class.StockInfo  import StockInfo
import information    as im

def main():

    while True:
        i = raw_input('>>> ').lower()
        if   i == '':                       pass
        elif i in ['e', 'exit', '99']:      break
        elif i in ['m', 'menu', 'l', 'ls']: showtip()
        elif i in ['c', 'clear']:           print('\n'*50)
        elif i in ['1', 'jbm']:             xg.main('jbm')
        elif i in ['2', 'hlp']:             xg.main('hlp')
        elif i in ['3', 'pzr']:             xg.main('pzr')
        elif i in ['4', 'pcr']:             xg.main('pcr')
        elif i in ['5', 'tor']:             xg.main('tor')
        
        elif i in ['11', 'ycx']:            xg.main('ycx')
        elif i in ['12', 'sdx', 'wdx']:     xg.main('sdx')
        elif i in ['13', 'tjd', 'wvd']:     xg.main('tjd')
        elif i in ['14', 'yyx']:            xg.main('yyx')
        elif i in ['15', 'ger']:            xg.main('ger')
        
        elif i in ['21', 'yxg']:            xg.main('yxg')
        elif i in ['22', 'gzg']:            xg.main('gzg')
        elif i in ['23', 'zxg']:            xg.main('zxg')
        elif i in ['24', 'ccg']:            xg.main('ccg')
        
        elif i in ['51', 'fd']:             cron.main()
        
        elif len(i) == 6:                   im.main(i)
        elif i in ['61', 'si']:             im.main()
        elif i in ['62', 'ge']:             pass
        else: print('your input content is wrong, please input again!')


def showtip():
    tip = '''
 在选股界面下可输入下列命令：
 1.添加股: add yxg|gzg|zxg|ccg 000001 000002 ...
 2.删除股: del yxg|gzg|zxg|ccg 000001 000002 ...
-------------------------------------------------------------------------------------------------------------
    [s]选股          [s]选股         [s]选股           [f]数据          [i]个股信息             [r]其他
 *1.基本面[jbm]  *11.阳穿线[ycx]  *21.预选股[yxg]  *51.下载数据[fd]  *61.个股信息[si]
 *2.高低价[hlp]  *12.双底形[sdx]  *22.观注股[gzg]  52.实时行情[分]    62.灰色预期[ge]
 *3.价资比[pzr]  *13.头肩底[tjd]  *24.自选股[zxg]  53.基金持股[季]                            32.添加自选股
 *4.价变率[pcr]  *14.阴阳线[yyx]  *23.持仓股[ccg]  54.龙虎榜单[日]                            98.执行SQL语句
 *5.换手率[tor]  *15.灰测率[ger]                   55.经营数据[周]                           *99.退出[e]
                                                   35.基金持自选股

'''
    print(tip)



if __name__ == '__main__':
    main()


