#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj


from datetime   import datetime
from Postgresql import Postgresql
from GreyExpect import GreyExpect


class XuanGu:
    def __init__(self, cs=None):
        self._ps      = Postgresql()
        self._xg      = 'all'
        self._cs      = [] if cs is None else cs
        self._dss     = [self.stock_list(f='tra')]  ### stored self._cs
        
        self._es      = []
        self._estitle = ''
        self._ispages      = False
        self._current_page = 1
        self._total_pages  = 1
        self._num_per_page = 25
        self._is_renew_cs  = True
        self._is_show_info = True
        
        self.title = 'all'
        self.zbj = {}
        self.zbj['jbm'] = ['pe', 'pb', 'esp', 'bvps', 'outs', 'amount', 'ds', 'ord', 'seq']
        self.zbj['hlp'] = ['nhr', 'lhr', 'nlr', 'ds', 'ord', 'seq']
        self.zbj['pzr'] = ['min_pzr', 'max_pzr', 'ds', 'ord', 'seq']
        self.zbj['pcr'] = ['minpcr', 'maxpcr', 'minlhr', 'maxlhr', 'ds', 'ord', 'seq']
        self.zbj['tor'] = ['n', 'mintor', 'maxtor', 'ds', 'ord', 'seq']
        self.zbj['xyx'] = ['pcr', 'percent', 'ord', 'seq']
        self.zbj['zdy'] = ['table', 'where', 'ds', 'ord', 'seq']
        
        self.zbj['ycx'] = ['n', 'ma', 'mb', 'mc', 'ds', 'ord', 'seq']
        self.zbj['sdx'] = ['minrate', 'maxrate', 'ds', 'ord', 'seq']
        self.zbj['tjd'] = ['min_rate', 'max_rate', 'ds', 'ord', 'seq']
        self.zbj['yyx'] = ['yindays', 'yangdays', 'ds', 'ord', 'seq']
        self.zbj['ger'] = ['ger', 'ds', 'ord', 'seq']
        
        self.zbj['all'] = ['ord', 'seq']
        self.zbj['tra'] = ['ord', 'seq']
        self.zbj['yxg'] = ['ord', 'seq']
        self.zbj['gzg'] = ['ord', 'seq']
        self.zbj['zxg'] = ['ord', 'seq']
        self.zbj['ccg'] = ['ord', 'seq']
        
        self.pps = {}
        #[]
        self.pps['ord']     = 'nhr'
        self.pps['seq']     = 'ASC'
        self.pps['ds']      = 'tradable'
        #[jbm]
        self.pps['pe']      = '200'
        self.pps['pb']      = '10'
        self.pps['esp']     = '0.01'
        self.pps['bvps']    = '1'
        self.pps['outs']    = '120'
        self.pps['amount']  = '0.6'
        #[hlp]
        self.pps['nhr']     = '0.6'
        self.pps['lhr']     = '0.5'
        self.pps['nlr']     = '0.4'
        #[pzr]
        self.pps['min_pzr'] = '0'       #pjr: price / jing_zi_chan * 100
        self.pps['max_pzr'] = '1.00'
        #[pcr]
        self.pps['minpcr']  = '1.0'
        self.pps['maxpcr']  = '5.0'
        self.pps['minlhr']  = '0'
        self.pps['maxlhr']  = '20'
        #[tor]
        self.pps['n']       = '1'
        self.pps['mintor']  = '20.0'
        self.pps['maxtor']  = '100.0'
        #[xyx]
        self.pps['pcr']= '-2.0'
        self.pps['percent'] = '0.5'
        #[zdy]
        self.pps['table']   = 'profit'
        self.pps['where']   = "code='600300'"
        #[ycx]
        self.pps['n']       = '1'
        self.pps['ma']      = 'ma5'
        self.pps['mb']      = 'ma10'
        self.pps['mc']      = 'ma20'
        #[sdx]
        self.pps['minrate'] = '0'
        self.pps['maxrate'] = '0.1'
        #[tjd]
        self.pps['min_rate'] = '0.1'
        self.pps['max_rate'] = '0.3'
        #[yyx]
        self.pps['yindays']  = '3'
        self.pps['yangdays'] = '1'
        #[ger]
        self.pps['ger']      = '0.9'
        
        
        

    def main(self, f='jbm'):
        self.title = f
        while True:
            starttime = datetime.now()
            if not self._is_show_info:
                self._is_renew_cs = False
            if self._is_renew_cs:
                if   self.title == 'jbm': self.ji_ben_mian()
                elif self.title == 'hlp': self.high_low_price()
                elif self.title == 'pzr': self.price_zi_rate()
                elif self.title == 'pcr': self.price_change_rate()
                elif self.title == 'tor': self.turn_over_rate()
                elif self.title == 'xyx': self.xia_ying_xian()
                elif self.title == 'zdy': self.zi_ding_yi()
                
                elif self.title == 'sdx': self.shuang_di_xing()
                elif self.title == 'tjd': self.tou_jian_di()
                elif self.title == 'ycx': self.yang_chuan_xian()
                elif self.title == 'yyx': self.yin_yang_xian()
                elif self.title == 'ger': self.gray_expect_rate()
                
                elif self.title == 'all': self.stock_list(f='all')
                elif self.title == 'tra': self.stock_list(f='tra')
                elif self.title == 'yxg': self.stock_list(f='yxg')
                elif self.title == 'gzg': self.stock_list(f='gzg')
                elif self.title == 'zxg': self.stock_list(f='zxg')
                elif self.title == 'ccg': self.stock_list(f='ccg')

            self._is_renew_cs  = True
            
            if self._is_show_info:
                self.show_info()
            self._is_show_info = True
            
            print '\033[1;31;40mTime:\033[0m %ss,' % str((datetime.now() - starttime))[-9:-4],
            i = self.show_tip()
            if i!='' and i in ['e', 'x', 'q', 'exit', 'quit']: break
            
    def display_select_stock(self):
        pass
    


    def show_info(self):
        if self._current_page > self._total_pages: self._current_page = self._total_pages
        cs_num = len(self._cs)
        if cs_num == 0:
            print('no reconders math condition, please renew conditions!')
            return
        self._es = [''] * cs_num if self._estitle == '' else self._es
        self._total_pages  = 1 if not self._ispages else (cs_num - 1) // self._num_per_page + 1
        
        title = '\n'*50 + '  NO  code    name      pcr    np    hp      lp   nhr  lhr  nlr pds/pks bds/bts pe  pb   esp  bvps  outs  tots  turn industry  concept area %s' % self._estitle
        title = title.replace(self.pps['ord'], '\033[1;31;40m%s\033[0m' % self.pps['ord'])
        print(title)
        stp = ''
        if len(self._cs) == 1:
            stp = "('%s')" % self._cs[0]    # otherwise ','
        else:
            stp = str(tuple(self._cs))
            
        sql = "SELECT code, name, pc, np, hp, lp, nhr, lhr, nlr, pds, pks, bds, bts, pe, pb, esp, bvps, outs, tots, turn, industry, concept, area "\
              "FROM profit WHERE code in %s ORDER BY %s %s" % (stp, self.pps['ord'], self.pps['seq'])
        startno = (self._current_page-1) * self._num_per_page
        if self._ispages:
            sql += " OFFSET %d LIMIT %d" % (startno, self._num_per_page)
        rs = self._ps.fetchall(sql)
        i = startno 
        rows = len(rs)
        for r in rs:
            i += 1
            if rows > self._num_per_page:   # for print '......'
                if i-startno == self._num_per_page - 1:
                    print('... ...')
                    continue
                if i-startno > self._num_per_page - 1 and i-startno < rows:
                    continue
            try:    
                print('%4d %6s %s %5.1f%% %6.2f %6.2f %6.2f %3.0f%% %3.0f%% %3.0f%% %2d/%-2d %2d/%-2d %5.1f %4.1f %5.2f %5.2f %5.1f %5.1f %4.1f%% %s %s %s %s'\
                      % (i, r[0], dk(r[1],8), r[2], r[3], r[4], r[5], r[6]*100, r[7]*100, r[8]*100, r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17]/10000, r[18]/10000, r[19], dk(r[20],8), dk(r[21],8), dk(r[22],4), self._es[i-1]))
            except Exception, data:
                print('some wrong')
                print(data)
                continue
            if i%5 == 0: print('')
        if (i)%5 > 0: print('')


    def show_tip(self):
        menu ='''\n\n\n ============ MENU ============

 exit:          ['e', 'x', 'q', 'exit', 'quit']:
 xuan_gu:       ['jbm', 'hlp', 'ycx', 'pcr', 'zdy', 'sdx', 'tjd', 'all', 'tra', 'yxg', 'zxg', 'ccg']
 order:         ['code', 'pc', 'np', 'hp', 'lp', 'nhr', 'lhr', 'nlr', 'pe', 'pb', 'esp', 'bvps', 'outs', 'tots', ...]
 sequence:      ['a', 'd', 'asc', 'desc']
 update_yxg:    ['y', 'yy']
 quick_upd_yxg: ['yr', 'replace', 'ya', 'append', 'yu', 'union']
 sel_data_set:  ['ds', 'dd', 'ss']
 quick_sel_dz:  ['da', 'dt', 'dz', 'dy', 'dc']
 page:          ['', 0-9]
 set_condition: 'value1, value2, value3,...' OR 'condition1=value, condition2=value, condition3=value, ...'
'''
        if self.title == 'all' :
            self._xg = 'all'
        elif self.title == 'tra':
            self._xg = 'all + tra'
        else:
            self._xg += ' + ' + self.title
        
        tip = '\033[1;31;40mPage:\033[0m %d/%d, \033[1;31;40mDateSet:\033[0m %s\n' % (self._current_page, self._total_pages, self._xg)
        tip += 'Please input parameters('
        for k in self.zbj[self.title]:
            tip += '%s=%s, ' % (k, self.pps[k]) 
        
        l = raw_input(tip.strip().rstrip(',')+'):').lower().split()
        if l == []: l = ['']
        i, n = l[0], len(l)
        if i in ['add']:
            cs = [l[j].strip(',') for j in range(2, n)]
            self.update_stock_list(field=l[1], value='true', codes=cs)
            print("add stock %s to '%s'" % (str(cs), l[1]))
            self._is_show_info = False
        elif i in ['del', 'delete']:
            cs = [l[j].strip(',') for j in range(2, n)]
            self.update_stock_list(field=l[1], value='false', codes=cs)
            print("delete stock %s from '%s'" % (str(cs), l[1]))
            self._is_show_info = False
        elif i in ['si', 'dsi']:
            cs = self._cs
            l.append('600300')
            self._cs = [l[1]]
            self.display_stock_info()
            self._cs = cs
            self._is_show_info = False
        elif i in ['m', 'menu', 'h', 'help', '?']:
            print(menu)
            self._is_show_info = False
        elif i == '' and not self._ispages:
            self._is_show_info = False
        elif i in ['e', 'x', 'q', 'exit', 'quit']:
            pass
        elif i in ['all', 'tra', 'jbm', 'hlp', 'pzr', 'pcr', 'tor', 'xyx', 'zdy', \
                   'ycx', 'sdx', 'tjd', 'yyx', 'ger', \
                   'yxg', 'gzg', 'zxg', 'ccg']:
            self.title = i
            self._current_page = 1
        elif i in ['y', 'yy', 'yr', 'replace', 'ya', 'append', 'yu', 'union']:
            if i == 'y' or i == 'yy':
                i = raw_input('>>> please input parameters([yr]:replace, [ya]:append, [yu]:union):')
            if   i == 'yr': i = 'replace'
            elif i == 'ya': i = 'append'
            elif i == 'yu': i = 'union'
            self.update_yu_xuan_gu(i)
            self._is_show_info = False
        elif i in ['a', 'd', 'asc', 'desc']:
            if   i == 'a': i = 'asc'
            elif i == 'd': i = 'desc'
            self.pps['seq'] = i.upper()
            self._is_renew_cs = False
        elif i in ['code', 'name', 'pc', 'np', 'hp', 'lp', 'nhr', 'lhr', 'nlr', 'pds', 'pks', 'bds', 'bts', 'pe', 'pb', 'esp', 'bvps', 'outs', 'tots', 'turn', 'industry', 'concept', 'area']:
            self.pps['ord'] = i
            self._is_renew_cs = False
        elif i in ['ds', 'dd', 'ss']:
            i = raw_input('>>> please select dz:[al, sh, sz, st, zxb, cyb, hssb, szwl, tradable, hold, zxg, yxg, ccg]:')
            if i in ['al','sh','sz','st','zxb','cyb','hssb','szwl','tradable','hold','zxg','yxg', 'ccg']:
                self.pps['ds'] = i
        elif i in ['da', 'dt', 'dz', 'dy', 'dc']:
            if   i == 'da': self.pps['ds'] = 'al'
            elif i == 'dt': self.pps['ds'] = 'tradable'
            elif i == 'dz': self.pps['ds'] = 'zxg'
            elif i == 'dy': self.pps['ds'] = 'yxg'
            elif i == 'dc': self.pps['ds'] = 'ccg'
        elif i in ['p', 'page', 'pages']:
            self._ispages = not self._ispages
            self._is_renew_cs = False
        elif i in ['m', 'menu']:
            pass
        elif i == '' and self._ispages:
            self._current_page += 1
            if self._current_page > self._total_pages: self._current_page = self._total_pages
            self._is_renew_cs = False
        elif all(c in "0123456789" for c in i) and self._ispages:
            self._current_page = 1 if int(i)<1 else int(i)
            if self._current_page > self._total_pages: self._current_page = self._total_pages
            self._is_renew_cs = False
        elif all(c in "0123456789.+-," for c in i):   #60，20...
            I = i.split(',')
            for j in range(len(I)):
                if I[j] == '' : continue
                self.pps[self.zbj[self.title][j]] = I[j]
        elif i.find('=')>0:
            Is = i.split(',')
            for I in Is:
                k = I.strip().split('=')
                self.pps[k[0]] = k[1]
        else: print('your input content is wrong, please input again!')
        return i


    def update_yu_xuan_gu(self, f='replace'):
        sql = ''
        if f == 'append':
            sql = "UPDATE stock_list SET yxg=TRUE WHERE code in %s;" % str(tuple(self._cs))
        elif f == 'replace':
            sql = "UPDATE stock_list SET yxg=FALSE;"\
                  "UPDATE stock_list SET yxg=TRUE WHERE code in %s;" % str(tuple(self._cs))
        elif f == 'union':
            sql = "UPDATE stock_list SET yxg=FALSE WHERE NOT (yxg and code in %s);" % str(tuple(self._cs))
        
        if f in ['replace', 'append', 'union']:
            self._ps.execute(sql)
            print('[%s] on field `yxg` of table `stock_list` is ok!' % f)
        else:
            print('update stock_list.yxg is failded!')


    def stock_list(self, f='all'):
        self.title = f
        if f == 'all' : f = 'al'
        elif f == 'tra' : f = 'tradable'
        sql = "SELECT code FROM stock_list WHERE %s;" % f
        return self._ps.fetchfield(sql)




    def ji_ben_mian(self):
        self.title = 'jbm'
        sql = "SELECT a.code FROM stock_list AS a LEFT JOIN profit AS b ON a.code=b.code "\
              "WHERE a.%s AND b.pe>0 AND b.pb>0 AND b.pe<%s AND b.pb<%s AND b.esp>%s "\
              "AND b.bvps>%s AND b.outs<%s*10000 AND b.np*b.vol>%s*1000000;"\
              % (self.pps['ds'], self.pps['pe'], self.pps['pb'], self.pps['esp'], self.pps['bvps'], self.pps['outs'], self.pps['amount'])
        rs = self._ps.fetchfield(sql)
        self._cs = list(set(self._dss[-1]).intersection(set(rs)))
    
    
    def high_low_price(self):
        self.title = 'hlp'
        sql = "SELECT a.code FROM stock_list AS a LEFT JOIN profit AS b ON a.code=b.code "\
              "WHERE a.%s AND b.lhr>0 AND b.lhr<%s AND b.nlr<%s AND b.nhr<%s;"\
              % (self.pps['ds'], self.pps['lhr'], self.pps['nlr'], self.pps['nhr'])
        rs = self._ps.fetchfield(sql)
        self._cs = list(set(self._dss[-1]).intersection(set(rs)))
    
    
    
    def price_zi_rate(self):
        self.title = 'pzr'
        sql = "SELECT a.code FROM stock_list AS a LEFT JOIN profit AS b ON a.code=b.code "\
              "WHERE a.%s AND b.np/(b.bvps+0.0001)>=%s AND b.np/(b.bvps+0.0001)<=%s;"\
              % (self.pps['ds'], self.pps['min_pzr'], self.pps['max_pzr'])
        rs = self._ps.fetchfield(sql)
        self._cs = list(set(self._dss[-1]).intersection(set(rs)))
    


    def price_change_rate(self):
        self.title = 'pcr'
        date = self._ps.fetchone("SELECT max(date) FROM data_hist;")[0]
        sql = "SELECT a.code FROM stock_list AS a LEFT JOIN data_hist AS b ON a.code=b.code "\
              "WHERE a.%s AND b.p_change>%s AND b.p_change<%s AND (b.high-b.low)/b.low>%s AND (b.high-b.low)/b.low<%s AND b.date='%s';"\
              % (self.pps['ds'], self.pps['minpcr'], self.pps['maxpcr'], self.pps['minlhr'], self.pps['maxlhr'], date)
        rs = self._ps.fetchfield(sql)
        self._cs = list(set(self._cs).intersection(set(rs)))
    


    def xia_ying_xian(self):
        self.title = 'xyx'
        date = self._ps.fetchone("SELECT max(date) FROM data_hist;")[0]
        sql = "SELECT a.code FROM stock_list AS a LEFT JOIN data_hist AS b ON a.code=b.code "\
                  "WHERE a.%s AND b.close<b.open AND b.p_change<=%s AND (b.close-b.low)/(b.high-b.low)>=%s AND b.date='%s';"\
                  % (self.pps['ds'], self.pps['pcr'], self.pps['percent'], date)
        self._cs = self._ps.fetchfield(sql)
        return True



    def zi_ding_yi(self):
        self.title = 'zdy'
        sql = "SELECT code FROM %s  WHERE %s;" % (self.pps['table'], self.pps['where'])
        try:
            self._cs = self._ps.fetchfield(sql)
        except Exception, data:
            print(data)
        return self._cs


    def turn_over_rate(self):
        self.title = 'tor'
        n = int(self.pps['n'])
        if n == 1:
            sql = "SELECT a.code FROM stock_list AS a LEFT JOIN profit AS b ON a.code=b.code "\
                  "WHERE a.%s AND turn>=%s AND turn<=%s;"\
                  % (self.pps['ds'], self.pps['mintor'], self.pps['maxtor'])
            rs = self._ps.fetchfield(sql)
            self._cs = list(set(self._cs).intersection(set(rs)))
            return True
        elif n > 1:
            cs = []
            for c in self._cs:
                sql = "SELECT turnover FROM data_hist WHERE code='%s' ORDER BY date DESC LIMIT %s;"\
                      % (c, self.pps['n'])
                rs = self._ps.fetchall(sql)
                f = True
                for r in rs:
                    if r[0] < float(self.pps['mintor']) or r[0] > float(self.pps['maxtor']):
                        f = False
                        break
                if f: cs.append(c)
            self._cs = cs
            return True
        else:
            return False



    def yang_chuan_xian(self):
        self.title = 'ycx'
        if self.pps['n'] == '1':
            date = self._ps.fetchone("SELECT max(date) FROM data_hist;")[0]
            sql = "SELECT a.code FROM stock_list AS a LEFT JOIN data_hist AS b ON a.code=b.code "\
                  "WHERE a.%s AND b.open<%s AND b.close>%s AND b.open<%s AND b.close>%s AND b.open<%s AND b.close>%s AND b.date='%s';"\
                  % (self.pps['ds'], self.pps['ma'], self.pps['ma'], self.pps['mb'], self.pps['mb'], self.pps['mc'], self.pps['mc'], date)
            rs = self._ps.fetchfield(sql)
            self._cs = list(set(self._cs).intersection(set(rs)))
            return True
        else:
            cs = []
            for c in self._cs:
                sql = "SELECT open, close, qfq, %s, %s, %s FROM data_hist WHERE code='%s' ORDER BY date DESC LIMIT %s;"\
                      % (self.pps['ma'], self.pps['mb'], self.pps['mc'], c, self.pps['n'])
                rs = self._ps.fetchall(sql)
                if len(rs) < int(self.pps['n']): continue
                opn, cls, ma, mb, mc, flag = 9999, 0, 0, 0, 0, True
                for r in rs:
                    tmp, tmb = r[0]*r[2], r[1]*r[2]
                    if tmp<opn: opn = tmp
                    if tmb>cls: cls = tmb
                    if opn > cls: flag = False; break
                    if ma == 0: ma = r[3]
                    if mb == 0: mb = r[4]
                    if mc == 0: mc = r[5]
                if flag and opn<ma and opn<mb and opn<mc and cls>ma and cls>mb and cls>mc:
                    cs.append(c)
            self._cs = cs
            return True


    def shuang_di_xing(self):
        self.title = 'sdx'
        cs = []
        for c in self._cs:
            sql = "SELECT low, qfq FROM data_hist WHERE code='%s' and isbott ORDER BY date DESC;" % c
            rs = self._ps.fetchall(sql)
            if len(rs)<2: continue
            r = (rs[0][0]*rs[0][1] - rs[1][0]*rs[1][1]) / rs[1][0]*rs[1][1]
            if r>float(self.pps['minrate']) and r<float(self.pps['maxrate']):
                cs.append(c)
        self._cs = cs
        return True


    def tou_jian_di(self):
        self.title = 'tjd'
        cs = []
        #  codes = self._ps.fetchfield("SELECT code FROM stock_list WHERE %s;" % self.pps['ds'])
        for c in self._cs:
            sql = "SELECT low, qfq FROM data_hist WHERE code='%s' and isbott ORDER BY date DESC;" % c
            rs = self._ps.fetchall(sql)
            if len(rs)<3: continue
            lr = (rs[2][0]*rs[2][1] - rs[1][0]*rs[1][1]) / rs[1][0]*rs[1][1]
            rr = (rs[0][0]*rs[0][1] - rs[1][0]*rs[1][1]) / rs[1][0]*rs[1][1]
            if lr>float(self.pps['min_rate']) and lr<float(self.pps['max_rate']) and rr>float(self.pps['min_rate']) and rr<float(self.pps['max_rate']):
                cs.append(c)
        self._cs = cs
        return True


    def yin_yang_xian(self):
        self.title = 'yyx'
        nyin  = int(self.pps['yindays'])
        nyang = int(self.pps['yangdays'])
        ny    = nyin + nyang
        cs = []
        for c in self._cs:
            sql = "SELECT open, close, price_change FROM data_hist WHERE code='%s' ORDER BY date DESC LIMIT %d;" % (c, ny)
            rs = self._ps.fetchall(sql)
            rrr = True
            sss = 0
            for r in rs:
                sss += 1
                if sss <= nyang:
                    if r[1] <= r[0]:
                        rrr = False
                        break
                else:
                    if r[2] > 0:
                        rrr = False
                        break
            if rrr: cs.append(c)
        self._cs = cs
        return True
    
    
    def gray_expect_rate(self):
        self.title = 'ger'
        ger = float(self.pps['ger'])
        ge  = GreyExpect()
        cs = []
        for c in self._cs:
            r = ge.positive_line_rate(c)
            if r > ger:
                cs.append(c)
        self._cs = cs
        return True
    

    def update_stock_list(self, field='gzg', value='true', codes=[]):
        cs  = str(codes).replace('[', '(').replace(']', ')')
        sql = "UPDATE stock_list SET %s=%s WHERE code in %s;" % (field, value, cs)
        self._ps.execute(sql)
        return True


    def display_stock_info(self):
        self.show_info()
        limit = 5
        sql = "SELECT date, close, price_change, p_change, volume, turnover, qfq FROM data_hist WHERE code='%s' ORDER BY date DESC LIMIT %d;" % (self._cs[0], limit)
        rs  = self._ps.fetchall(sql)
        if rs is None: return
        print('    date      close     pc      pcr    volume   turnover')
        for r in rs:
            print(' %s %7.2f %7.2f %7.2f%% %8.0f %7.2f%%' % (r[0], r[1]*r[6], r[2], r[3], r[4], r[5]))
        print('')


def dk(v='', k=10):
    vks = []
    for s in v.decode('utf-8'):
        inside_code=ord(s)
        if inside_code<0x0020 or inside_code>0x7e:  #是否为全角
            vks.append(2)
        else:
            vks.append(1)
    length = sum(vks)
    fn = len(vks)
    if length > k:
        for s in v.decode('utf-8'):
            if vks[0] == 2:
                v = v[(vks[0]+1):]
            else:
                v = v[vks[0]:]
            vks.pop(0)
            if sum(vks) <= k:
                break
    return  ' ' * (k - sum(vks)) + v


'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def dk1(v='', k=10):
    value = u'%s' % v
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length)/2 + length
    if length > k:
        return v[length-k+1:]
    else:
        return  ' ' * (k - length) + v
'''




if __name__ == '__main__':

    pass




