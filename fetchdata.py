#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author hhj


import sys, time, datetime
import tushare as ts
import pandas as pd
from Class.Postgresql import *      # Postgresql Sqlalchemy
from Class import getinfo
from function import base as fb

sq = Sqlalchemy()
ENGINE = sq.create_engine()

def fetch_data_hist():
    today = datetime.date.today()
    weekday = today.weekday()
    if weekday==5: today -= datetime.timedelta(days=1)
    elif weekday==6: today -= datetime.timedelta(days=2)

    ps = Postgresql()
    cs = getinfo.get_codes(fields=['tradable'])
    i, s = 0, len(cs)
    for c in cs:
        starttime = datetime.datetime.now()
        i += 1
        r = ps.fetchone("SELECT max(date) FROM data_hist WHERE code='%s'" % c)
        if r[0]:
            date = r[0] + datetime.timedelta(days=1)
            if date > today: 
                print('[%d/%d=%.1f%%] %s price is newly!'%(i, s, float(i)/float(s)*100, c))
                continue
            try:
                df = ts.get_hist_data(c, start=str(date))
            except Exception as data:
                print(data)

            if df is None: 
                print('[%d/%d=%.1f%%] %s price is newly!'%(i, s, float(i)/float(s)*100, c))
                continue 
        else:
            try:
                df = ts.get_hist_data(c)
            except Exception as data:
                print(data)
        df.insert(0, 'code', pd.Series([c], index=df.index))
        df.to_sql('data_hist', ENGINE, if_exists='append')
        endtime = datetime.datetime.now()
        print('[%d/%d=%.1f%%] fetching %s stock prices! time=[%s]'%(i, s, float(i)/float(s)*100, c, endtime-starttime))
    ps.close()
    print('stock histroy prices is fetched!')



def fetch_stock_basics():
    fb.write('start fetching stock basic info ...')
    df = ts.get_stock_basics()
    df.to_sql('stock_basics', ENGINE, if_exists='replace')
    print('is done!')

    fb.write('start copying code and name from table [stock_basics] to table [stock_list] ...')
    ps = Postgresql()
    '''
    rs = ps.fetchall("SELECT code, name FROM stock_basics ORDER BY code ASC;")
    for r in  rs:
        ps.update_insert(table='stock_list', where="code='%s'"%r[0], code=r[0], name=r[1])
    fb.write(' is done!\n')
    
    fb.write('start fleshing hushi shenshi chuangyeban zhongxiaoban code ...')
    sql = "UPDATE stock_list SET sh=TRUE WHERE substr(code,1,1)='6';"\
          "UPDATE stock_list SET sz=TRUE WHERE substr(code,1,1)='0' OR substr(code,1,1)='3';"\
          "UPDATE stock_list SET cyb=TRUE WHERE substr(code,1,1)='3';"\
          "UPDATE stock_list SET zxb=TRUE WHERE substr(code,1,3)='002';"
    ps.execute(sql)
    fb.write(' is done!\n')
    
    fb.write('start fetching ST stock code ...')
    sql = ''
    for vs in ts.get_st_classified().values:
        sql += "UPDATE stock_list SET st=TRUE WHERE code='%s';"%vs[0]
    ps.execute(sql)
    fb.write(' is done!\n')

    fb.write('start fetching hushen 300 stock code...')
    sql = ''
    for vs in ts.get_hs300s().values:
        sql += "UPDATE stock_list SET hssb=TRUE WHERE code='%s';"%vs[0]
    ps.execute(sql)
    fb.write('is done!\n')
    
    fb.write('start fetching shangzheng 50 stock code...')
    sql = ''
    for vs in ts.get_sz50s().values:
        sql += "UPDATE stock_list SET szwl=TRUE WHERE code='%s';"%vs[0]
    ps.execute(sql)
    fb.write('is done!\n')

    fb.write('start fetching tradable stocke code ...')
    sql = ''
    for vs in ts.get_today_all().values:
        sql += "UPDATE stock_list SET tradable=TRUE WHERE code='%s';"%vs[0]
    ps.execute(sql)
    fb.write(' is done!\n')
    
    
    fb.write('start fetching stock industry class...')
    sql = ''
    for vs in ts.get_industry_classified().values:
        sql += "UPDATE stock_list SET industry='%s' WHERE code='%s';" % (vs[2], vs[0])
    ps.execute(sql)
    fb.write(' is done!\n')
    '''    
    fb.write('start fetching stock concept class...')
    sql = ''
    for vs in ts.get_concept_classified().values:
        sql += "UPDATE stock_list SET concept='%s' WHERE code='%s';" % (vs[2], vs[0])
        sql += "UPDATE profit SET concept='%s' WHERE code='%s';" % (vs[2], vs[0])
    ps.execute(sql)
    fb.write(' is done!\n')
    
    fb.write('start fetching stock area class...')
    sql = ''
    for vs in ts.get_area_classified().values:
        sql += "UPDATE stock_list SET area='%s' WHERE code='%s';" % (vs[2], vs[0])
    ps.execute(sql)
    fb.write(' is done!\n')
    
    ps.close()
#    reflesh_profit_stock_info()











def fetch_realtime_quotes(cs=['sh', 'sz', '600300', '601633']):
    ps = Postgresql()
    df = ts.get_realtime_quotes(cs)
    for r in df.values:
        for i in range(10, 30):
            if r[i] == '': r[i] = 0
        ps.update_insert(table='data_realtime', where="date='%s' and time='%s' and code='%s'" % (r[30], r[31], r[32]), \
                        date=str(r[30]), time=str(r[31]), code=str(r[32]), open=r[1], pre_close=r[2], price=r[3], \
                        high=r[4], low=r[5], bid=r[6], ask=r[7], volume=r[8], amount=r[9], \
                        b1_v=r[10], b1_p=r[11], b2_v=r[12], b2_p=r[13], b3_v=r[14], b3_p=r[15], b4_v=r[16], b4_p=r[17], b5_v=r[18], b5_p=r[19], \
                        a1_v=r[20], a1_p=r[21], a2_v=r[22], a2_p=r[23], a3_v=r[24], a3_p=r[25], a4_v=r[26], a4_p=r[27], a5_v=r[28], a5_p=r[29])
    ps.close()


def fetch_fund_holdings():
    '''基金持股'''
    df = ts.fund_holdings(2015, 1)
    sql = ''
    for r in df.values:
        cur.execute("SELECT code FROM stock_fund_holdings WHERE code='%s' AND date='%s';"%(r[0], r[2]))
        R = cur.fetchone()
        if R is None:
            sql += "INSERT INTO stock_fund_holdings (code, name, date, nums, nlast, count, clast, amount, ratio) VALUES ('%s', '%s', '%s', '%d', '%d', '%f', '%f', '%f', '%f');"%(r[0], r[1], r[2], int(r[3]), int(r[4]), float(r[5]), float(r[6]), float(r[7]), float(r[8]))
        else:
            sql += "UPDATE stock_fund_holdings SET nums=%d, nlast=%d, count=%f, clast=%f, amount=%f, ratio=%f WHERE code='%s' AND date='%s';"%(int(r[3]), int(r[4]), float(r[5]), float(r[6]), float(r[7]), float(r[8]), r[0], r[2])
        sql += "UPDATE stock_list SET jjcg=true WHERE code='%s';"%r[0]
    cur.execute(sql)
    conn.commit()
    fb.write(' is done!\n')
#    df.to_sql('fund_holdings', ENGINE, if_exists='replace')








############################# analyse data #############################
def reflesh_profit_stock_info():
    fb.write('start refleshing stock info on table [profit] .')
    ps = Postgresql()
    sql = "SELECT code, name, industry, area, bvps, esp, outstanding, totals, \"timeToMarket\" FROM stock_basics ORDER BY code"
    rs = ps.fetchall(sql)
    i = 0
    for r in rs:
        ps.update_insert(table='profit', where="code='%s'"%r[0], code=r[0], name=r[1], industry=r[2],
                         area=r[3], bvps=r[4], esp=r[5], outs=r[6], tots=r[7], market=str(r[8]))
        i += 1
        if i%100 == 0:
            fb.write('.')
    ps.close()
    fb.write(' is done!\n')



def reflesh_data_hist_fq():
    print('start refleshing hfq & qfq values on table [data_hist] ...')
    ps = Postgresql()
    rs = ps.fetchall("SELECT DISTINCT code FROM data_hist ORDER BY code;")
    j, jj, s = 0, 0, len(rs)
    for r in rs:
        starttime = datetime.datetime.now()
        c = r[0]
        j += 1
        date = '1975-09-02'
        #r = ps.fetchone("SELECT date FROM data_hist WHERE code='%s' AND hfq>0 ORDER BY date DESC LIMIT 1;" % c)
        r = ps.fetchone("SELECT max(date) FROM data_hist WHERE code='%s' AND hfq>0;" % c)
        if r[0] is not None:   # if r: = if r is not None:
            date = r[0]
        else:
            tmp = ps.fetchone("SELECT min(date) FROM data_hist WHERE code='%s';" % c)
            if tmp[0] is None: continue
            date = tmp[0]
            ps.execute("UPDATE data_hist SET hfq=1 WHERE code='%s' AND date='%s';" % (c, date))
        # start set hfq value
        b_cls, b_hfq, hfq, i, sql = 0, 0, 0, 0, ''
        rs = ps.fetchall("SELECT date, close, price_change, hfq FROM data_hist WHERE code='%s' AND date>='%s' ORDER BY date;" % (c, date))
        if rs is not None:
            for R in rs:
                i += 1
                cls, pcg = float(R[1]), float(R[2])
                if i == 1:
                    hfq = R[3]
                else:
                    if cls - pcg - b_cls < -0.02:  
                        hfq = b_cls / (cls - pcg) * b_hfq
                    else:
                        hfq = b_hfq
                    sql += "UPDATE data_hist SET hfq=%f WHERE code='%s' AND date='%s';" % (hfq, c, R[0])
                b_cls = cls
                b_hfq = hfq
       
        # start set qfq value
        mr  = ps.fetchone("SELECT hfq FROM data_hist WHERE code='%s' AND qfq is null ORDER BY date DESC" % c)     #second newly hfq
        if mr is not None:
            if hfq == mr[0]:
                sql += "UPDATE data_hist SET qfq=hfq/%f WHERE code='%s' AND qfq is null;" % (hfq, c)
            else:
                sql += "UPDATE data_hist SET qfq=hfq/%f WHERE code='%s';" % (hfq, c)
            if sql != '': ps.execute(sql)
        endtime = datetime.datetime.now()
        print('[%d/%d=%.1f%%] [%s] hfq & qfq values is computed and saved! time=[%s]' % (j, s, float(j)/float(s)*100, c, endtime-starttime))
    print('all hfq & qfq data on table [data_hist] computed and saved!')



def identify_data_hist_price_wave(periods=10, start='2015-05-01'):
    ps = Postgresql()
    cs = getinfo.get_codes()
    i, s = 0, len(cs)
    for c in cs:
        starttime = datetime.datetime.now()
        i += 1
        sql = "SELECT date, close, qfq, high, low FROM data_hist WHERE code='%s' AND date>='%s' ORDER BY date DESC"%(c, start)
        rs = ps.fetchall(sql)
        rows = len(rs)
        if rows<=periods:
            continue
        sql = "UPDATE data_hist SET ispeak=null, isbott=null WHERE (ispeak OR isbott) AND code='%s';"%c
        for j in range(rows-periods):
            ispeak = isbott = True
            for k in range(1, periods+1):
                j_k = max([j-k, 0])
                hn = rs[j][3]   * rs[j][2]
                hb = rs[j+k][3] * rs[j+k][2]
                ha = rs[j_k][3] * rs[j_k][2]
                ln = rs[j][4]   * rs[j][2]
                lb = rs[j+k][4] * rs[j+k][2]
                la = rs[j_k][4] * rs[j_k][2]
                if hn<=hb or hn<ha: ispeak = False
                if ln>=lb or ln>la: isbott = False
            if ispeak:
                sql += "UPDATE data_hist SET ispeak=true WHERE code='%s' AND date='%s';" % (c, rs[j][0])
            if isbott:
                sql += "UPDATE data_hist SET isbott=true WHERE code='%s' AND date='%s';" % (c, rs[j][0])
        ps.execute(sql)
        endtime = datetime.datetime.now()
        print("[%d/%d=%.1f%%] [%s] ispeak and isbott are identified! time=[%s]" % (i, s, float(i)/float(s)*100, c, endtime-starttime))
    ps.close()
    print('is ok')


def reflesh_profit_peaks_botts():
    ps = Postgresql()
    cs = getinfo.get_codes()
    SQL, i, s = '', 0, len(cs)
    for c in cs:
        i += 1
        r  = ps.fetchone("SELECT count(ispeak), count(isbott) FROM data_hist WHERE code='%s';" % c)
        ra = ps.fetchone("select count(*) from data_hist where code='%s' and date>= (select max(date) from data_hist where code='%s' and ispeak)" % (c, c))
        rb = ps.fetchone("select count(*) from data_hist where code='%s' and date>= (select max(date) from data_hist where code='%s' and isbott)" % (c, c))
        SQL += "UPDATE profit SET pks=%f, bts=%f, pds=%f, bds=%f WHERE code='%s';"%(r[0], r[1], ra[0], rb[0], c)
        print("[%d/%d=%.1f%%] [%s] the number of peak or bott is counted!"%(i, s, float(i)/float(s)*100, c))
    ps.execute(SQL)
    ps.close()
    print('is ok!')



def reflesh_profit_prices(codes=getinfo.get_codes(), start='2015-05-01'):
    print('start reflashing newly hightest and lowest price on table [profit]')
    ps = Postgresql()
    SQL, i, s = '', 0, len(codes)
    for c in codes:
        i += 1
        sql = "SELECT p_change, close, volume, turnover FROM data_hist WHERE code='%s' AND date>='%s' ORDER BY date DESC LIMIT 1"%(c, start)
        r = ps.fetchone(sql)
        if r is None: continue
        pc, np, vol, turn = r[0], r[1], r[2], r[3]
        sql = "SELECT max(high*qfq), min(low*qfq) FROM data_hist WHERE code='%s' AND date>='%s'"%(c, start)
        r = ps.fetchone(sql)
        hp, lp = r[0], r[1]        
        SQL += "UPDATE profit SET hp=%.2f, lp=%.2f, np=%.2f, lhr=%f, nlr=%f, nhr=%f, vol=%f, turn=%f, pc=%f "\
               "WHERE code='%s';"%(hp, lp, np, lp/hp, (np-lp)/lp, np/hp, vol, turn, pc, c)
        print('[%d/%d=%.1f%%] [%s] stock prices info computed!'%(i, s, float(i)/float(s)*100, c))
    ps.execute(SQL)
    print('all stock newly prices info is saved into table [profit]')
    fb.write('start reflashing pe & pb ... ')
    SQL  = "UPDATE profit SET pb=np/bvps WHERE bvps!=0;"
    SQL += "UPDATE profit SET pe=np/esp WHERE esp!=0;"
    ps.execute(SQL)
    print(' is done!')







if __name__ == '__main__':

    fetch_stock_basics()



