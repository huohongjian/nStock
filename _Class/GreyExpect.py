#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj


import time
from Postgresql import Postgresql


class GreyExpect:
    
    def __init__(self):
        self.sum    = 30    # yang_ben_zong_shu_liang
        self.dates  = []    # yang_ben_dates
        self.isxzj  = True  # is_xia_zai_ji
        self.ybj    = []    # yang_ben_ji
        self.ybn    = 5     # yang_ben_shu
        self.ycn    = 2     # yu_ce_shu
        self.ps     = Postgresql()
    
    def main(self, code='600300'):
        self.get_dataset(code)
        self.show_head()
        self.show_body(zbj=self.ybj)
        
        for f in [True, False]:
            self.isxzj = f
            self.get_dataset(code)
            for i in [4, 5, 6]:
                if i>len(self.ybj): break
                ycj = self.yu_ce(ybj=self.ybj[-i:], ycn=3)
                self.show_body(zbj=ycj)
        self.isxzj = True


    def show_head(self):
        for i in range(1, self.sum + 11):
            p = '+' + str(i - self.sum) if i > self.sum else str(i)
            print '%2s' % p,
        print
        
        for d in self.dates:
            print '%2s' % d.day,
        print
        
        w = ['SU', 'MO', 'TU', 'ME', 'TR', 'FR', 'SA']
        for d in self.dates:
            print '%2s' % w[d.isoweekday()],
        print
        
    
    
    def show_body(self, zbj=[]):
        fs = [' \033[1;31;40m□\033[0m', ' \033[0;32;40m■\033[0m']
        if self.isxzj: fs.reverse() 
        for i in range(1, self.sum + 11):
            if i>=zbj[0] and (i<=max(zbj) or i<=self.sum):
                f = fs[0] if i in zbj else fs[1]
                print '%s' % f,
            else:
                print '  ',
        word = ' [xzj]' if self.isxzj else ' [ybj]'
        print word
    
    
    def pan_duan_jing_du(self, ybj=[], ycj=[]):
        
        ybn = len(ybj)
        q = (sum(ybj) - sum(ycj)) / float(ybn)     # can_cha_ping_jun_zhi
        q2, i = 0.0, 0                             # can_cha_de_fang_cha
        rmax = [0, 0.0]
        rmin = [0, 0.0]
        for k, v in zip(ybj, ycj):
            kv = k - v
            q2 += (kv - q) ** 2
 #           print k, '-', v, '=', k-v
            if kv > rmax[1]:
                rmax[0] = i
                rmax[1] = kv
            if kv < rmin[1]:
                rmin[0] = i
                rmin[1] = kv
            i += 1
        S2 = (q2 / float(ybn)) ** 0.5
        
        q = sum(ybj) / float(ybn)
        l = s = 0
        for v in ybj:
            l  += v
            s += (l - q) ** 2
        S1 = (s / float(ybn)) ** 0.5
        print ' C = %6.4f, when C<0.35, yu ce jing du jiao gao!' % (S2/S1)


    def yu_ce(self, ybj=[], ycn=2):
        yc1 = self.model(ybj=ybj, ycn=ycn)
        qs = [(k-v) for k, v in zip(ybj, yc1)]
        yc2 = self.model(ybj=qs, ycn=ycn)
        ycj = [int(k+v) for k, v in zip(yc1, yc2)]
        return ycj
        
 
    def model(self, ybj=[], ycn=2):                  # ybj:yang_ben_ji  ycn:yu_ce_number
        k = l = a = b = c = d = bt = by = pre = 0.0
        BS = []
        ybn = len(ybj)
        for i in range(ybn-1):
            k += float(ybj[i])
            l  = k + float(ybj[i+1])
            v  = -(k + l) / 2.0
            BS.append(v)

        for B in BS:
            a, b, c, d = a+B*B, b+B, c+B, d+1
        D = a*d - b*c
        B = [d/D, -b/D, -c/D, a/D]

        for k, v in zip(BS, ybj[1:]):
            bt += k * v
            by += v
        va = B[0] * bt + B[1] * by
        vv = B[2] * bt + B[3] * by
        vd = vv/va
        
        ycj = []
        for i in range(ybn + ycn):
            res = (ybj[0] - vd) * (2.718281828459045 ** (-va*i)) + vd
            ycj.append(res-pre)
            pre = res
        return ycj
        
        

    def get_dataset(self, code='600300'):
        self.ybj, self.dates = [], []
        sql = "SELECT open, close, date, price_change FROM data_hist WHERE code='%s' ORDER BY date DESC LIMIT %d;" % (code, self.sum)
        rs  = self.ps.fetchall(sql)
        i = 0
        for r in rs:
            if self.isxzj and r[3]<0:
                self.ybj.append(self.sum - i)
            elif not self.isxzj and r[3]>=0:
                self.ybj.append(self.sum - i)
            i += 1
            self.dates.append(r[2])
        self.ybj.reverse()
        self.dates.reverse()

    def positive_line_rate(self, code='600300', n=1):     # get the rate of positive line when next day
        s = j = 0.0
        for f in [True, False]:
            self.isxzj = f
            self.get_dataset(code)
            for i in [5, 7, 9]:
                if i>len(self.ybj): break
                ycj = self.yu_ce(ybj=self.ybj[-i:], ycn=2)
                s +=1
                if self.isxzj and (self.sum+n) not in ycj:
                    j +=1
                elif not self.isxzj and (self.sum+n) in ycj:
                    j +=1
        self.isxzj = True
        return j/s


if __name__ == '__main__':
    ge = GreyExpect()
    r = ge.positive_line_rate()
    print r