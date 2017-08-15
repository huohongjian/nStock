#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj

import cron
from Class.XuanGu     import XuanGu
from Class.StockInfo  import StockInfo
from Class            import Trade
import information    as im

def main():
    print('\n'*30)
    xg = XuanGu()
    is_showtip = True
    while True:
        if is_showtip:
            showtip()
        is_showtip = True
        inp  = raw_input('>>> ').lower()
        inps = inp.split()
        if inps == []: inps = ['']
        i = inps[0]
        n = len(inps)
        if   i == '': is_showtip = False
        elif i in ['e', 'exit', '99']:      break
        elif i in ['m', 'menu', 'l', 'ls']: showtip()
        elif i in ['c', 'clear']:           print('\n'*50)
        elif i in ['1', 'jbm']:             xg.main('jbm')
        elif i in ['2', 'hlp']:             xg.main('hlp')
        elif i in ['3', 'pzr']:             xg.main('pzr')
        elif i in ['4', 'pcr']:             xg.main('pcr')
        elif i in ['5', 'tor']:             xg.main('tor')
        elif i in ['6', 'xyx']:             xg.main('xyx')
        elif i in ['9', 'zdy']:             xg.main('zdy')
        
        elif i in ['11', 'ycx']:            xg.main('ycx')
        elif i in ['12', 'sdx', 'wdx']:     xg.main('sdx')
        elif i in ['13', 'tjd', 'wvd']:     xg.main('tjd')
        elif i in ['14', 'yyx']:            xg.main('yyx')
        elif i in ['15', 'ger']:            xg.main('ger')
        
        elif i in ['21', 'all', 'a']:       xg.main('all')
        elif i in ['22', 'tra', 't']:       xg.main('tra')
        elif i in ['26', 'yxg']:            xg.main('yxg')
        elif i in ['27', 'gzg']:            xg.main('gzg')
        elif i in ['28', 'zxg']:            xg.main('zxg')
        elif i in ['29', 'ccg']:            xg.main('ccg')
        
        elif i in ['51', 'fd']:             cron.main()
        
        elif len(i) == 6:                   im.main(i)
        elif i in ['61', 'si']:             im.main()
        elif i in ['62', 'ge']:             pass
        elif i in ['66', 'se']:             xg.main('se')
        elif i in ['67', 'ud']:             xg.main('ud')
        
        elif i in ['91', 'tr']:             Trade.main()
        
        else: print('your input content is wrong, please input again!')


def showtip():
    tip = '''
 在选股界面下可输入下列命令：
 1.添加股: add yxg|gzg|zxg|ccg 000001 000002 ...
 2.删除股: del yxg|gzg|zxg|ccg 000001 000002 ...

-------------------------------------------------------------------------------------------------------------
    [s]选股          [s]选股         [s]选股         [c]组合选股      [f]数据          [i]个股信息         [r]其他
 *1.基本面[jbm]  *11.阳穿线[ycx]  *21.全部股[all]   31.            *51.下载数据[fd]  *61.个股信息[si]  *91.交易数据[tr]
 *2.高低价[hlp]  *12.双底形[sdx]  *22.交易股[tra]   32.             52.实时行情[分]   62.灰色预期[ge]
 *3.价资比[pzr]  *13.头肩底[tjd]  *23.              33.             53.基金持股[季]                     32.添加自选股
 *4.价变率[pcr]  *14.阴阳线[yyx]  *24.              34.             54.龙虎榜单[日]                     98.执行SQL语句
 *5.换手率[tor]  *15.灰测率[ger]                                    55.经营数据[周]                    *99.退出[e]
 
 *6.下影线[xyx]                   *26.预选股[yxg]                                    *66.已选股票[se]
 *9.自定义[zdy]                   *27.观注股[gzg]                 35.基金持自选股    *67.撤销选择[ud]
                                  *28.自选股[zxg]
                                  *29.持仓股[ccg]
 
'''
    print(tip)



if __name__ == '__main__':
    main()


