#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj


import time, sys
import tushare as ts


def main():
    args = sys.argv if len(sys.argv) > 1 else ['monitor.py', '000776:1000:100', '300347:2000:50']
    args.pop(0)
    
    print '  NO    time     code   price    pc     pcr   valume  amount  bid    ask'

    valumes, amounts, valumec, amountc, codes = {}, {}, {}, {}, []
    for arg in args:
        lst = arg.split(':') + ['0']*2
        c = lst[0]
        codes.append(c)
        valumec[c] = 1000 if lst[1] == '0' else int(lst[1])
        amountc[c] = 100  if lst[2] == '0' else int(lst[2])
        valumes[c] = 0
        amounts[c] = 0
    
    i = 0
    while True:
        time.sleep(2)
        t = time.strftime("%H:%M:%S")
        if (t > '09:28:00' and t < '11:38:00') or (t > '12:58:00' and t < '23:08:00'):
            try:
                df = ts.get_realtime_quotes(codes)
            except:
                continue
        else:
            time.sleep(60)
            continue
        for r in df.values:
            open, pre_close, price, high, low, bid, ask = float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6]), float(r[7])
            volume, amount = float(r[8])/100, float(r[9])/10000
            b1_v, b2_v, b3_v, b4_v, b5_v = r[10], r[12], r[14], r[16], r[18]
            b1_p, b2_p, b3_p, b4_p, b5_p = r[11], r[13], r[15], r[17], r[19]
            a1_v, a2_v, a3_v, a4_v, a5_v = r[20], r[22], r[24], r[26], r[28]
            a1_p, a2_p, a3_p, a4_p, a5_p = r[21], r[23], r[25], r[27], r[29]
            date, times, code =str(r[30]), str(r[31]), str(r[32])

            vc = volume - valumes[code]
            ac = amount - amounts[code]
            valumes[code] = volume
            amounts[code] = amount
            pc  = price - pre_close
            pcr = pc / pre_close * 100
            if vc > valumec[code] or ac > amountc[code]:
                i += 1
                print ' %3d  %s  %s  %5.2f %6.2f %5.1f%% %7.0f %6.0f %6.2f %6.2f' % (i, times, code, price, pc, pcr, vc, ac, bid, ask), '\a'
                if i%5 == 0: print('')



if __name__ == '__main__':
    main()