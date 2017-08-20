#encoding:utf-8
#author:hhj


from datetime   import datetime
from Postgresql import Postgresql
from XuanGu     import XuanGu


class Trade:
    def __init__(self):
        self.ps     = Postgresql()
        self.code   = '600300'
        self.tax    = 0.001
        self.charge = 0.0003



    def _analyse(self, ps=['buy', '600300', '100.00', '100', '2015-12-30', '5']):
        fs = {'fun':'', 'code':'', 'price':0.0, 'amount':100, 'date':datetime.now(), 'other':[]}
        for p in ps:
            if p.isalpha():
                fs['fun'] = p
            elif len(p)==6 and p[:3] in ['600', '601', '603', '000', '002', '300']:
                fs['code'] = p
            elif '-' in p:
                fs['date'] = p
            elif '.' in p:
                fs['price'] = float(p)
            elif float(p)%100 == 0:
                fs['amount'] = int(p)
            else:
                fs['other'] += [p]
        if fs['code'] != '':
            self.code = fs['code']
        return fs
    
    
    def buy(self, ps=['buy', '600300', '100.00', '100', '2015-12-30']):
        fs = self._analyse(ps)
        if fs['price'] == 0.0 or fs['amount'] == 0:
            print 'some your input content is wrong, please input again!'
            return
        sums    = fs['price'] * fs['amount']
        charge  = max(5, sums * self.charge)
        cost    = sums + charge
        sql = "INSERT INTO trade (code, bprice, bamount, cost, bdate, position) VALUES ('%s', %.2f, %f, %.2f, '%s', %f) RETURNING id;" \
              % (self.code, fs['price'], fs['amount'], cost, fs['date'], fs['amount'])
        idno = self.ps.execute(sql)
        return idno
    
    
    def sale(self, ps=['sale', '600300', '100.00', '100', '2015-12-30']):
        fs = self._analyse(ps)
        if fs['price'] == 0.0 or fs['amount'] == 0:
            print 'some your input content is wrong, please input again!'
            return
        sums    = fs['price'] * fs['amount']
        charge  = max(5, sums * self.charge)
        tax     = sums * self.tax
        income  = sums - charge - tax
        sql = "INSERT INTO trade (code, sprice, samount, income, sdate, position) VALUES ('%s', %.2f, %f, %.2f, '%s', %f) RETURNING id;" \
              % (self.code, fs['price'], fs['amount'], income, fs['date'], -fs['amount'])
        idno = self.ps.execute(sql)
        return idno
    
    
    def combinebycode(self, ps=['combinebycode', '600300']):
        fs = self._analyse(ps)
        code = self.code
        limit = '2' if len(fs['other'])==0 else fs['other'][0]
        sql = "SELECT id FROM trade WHERE code='%s' and position!=0 ORDER BY id DESC LIMIT %s;" % (code, limit)
        res = self.ps.fetchfield(sql)
        ids = [str(r) for r in res]
        self.combine(['combine']+ids)
    
    
    def combine(self, ps=['combine', '5', '6', '8']):
        '''he bing ji lu'''
        ids = ps[1:]
        idn = len(ids)
        if idn < 2:
            print('please input two and more ids...')
            return False
        
        ids.sort(reverse=True)
        idstr = ','.join(ids)
        sql = "SELECT SUM(bamount), SUM(cost), MAX(bdate), SUM(samount), SUM(income), MAX(sdate), SUM(position) FROM trade WHERE id IN (%s);" % idstr
        res = self.ps.fetchone(sql)
        
        bamount, cost, bdate, samount, income, sdate, position = res[0], res[1], res[2], res[3], res[4], res[5], res[6]
        
        bcharge = max(5, cost / (1 + self.charge) * self.charge)
        bprice  = 0.00 if bamount == 0 else (cost - bcharge) / bamount
        scharge = max(5, income / (1 - self.charge - self.tax) * self.charge)
        stax    = income / (1 - self.charge - self.tax) * self.tax
        sprice  = 0.00 if samount == 0 else (income + scharge + stax) / samount
        
        sql = "UPDATE trade SET bprice=%.2f, bamount=%f, cost=%.2f,   bdate='%s', \
                                sprice=%.2f, samount=%f, income=%.2f, sdate='%s', position=%f WHERE id=%s;" \
              % (bprice, bamount, cost, bdate, sprice, samount, income, sdate, position, ids[0])
        sql += "DELETE FROM trade WHERE id IN (%s);" % ','.join(ids[1:])
        self.ps.execute(sql)
        
        self.split(int(ids[0]))
        
        
    def split(self, idno=-1):
        sql = "SELECT code, bprice, bamount, cost, bdate, sprice, samount, income, sdate FROM trade WHERE id=%d;" % idno
        r   = self.ps.fetchone(sql)
        code, bprice, bamount, cost, bdate, sprice, samount, income, sdate = r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]
        if bamount == 0 or samount == 0:
            print('can not slpit!')
            return
        if bamount == samount:
            sql = "UPDATE trade SET profit=income-cost WHERE id=%d;" % idno
            self.ps.execute(sql)
            return
        
        balance = {'bamount':0, 'cost':0.0, 'samount':0, 'income':0.0}
        if bamount > samount:
            balance['bamount']  = bamount - samount
            balance['cost']     = cost / bamount * balance['bamount']
            bamount -= balance['bamount']
            cost    -= balance['cost']
            sprice  = 0
        elif bamount < samount:
            balance['samount']  = samount - bamount
            balance['income']   = income / samount * balance['samount']
            samount -= balance['samount']
            income  -= balance['income']
            bprice  = 0
        
        sql = "UPDATE trade SET bamount=%f, cost=%.2f, samount=%f, income=%.2f, position=0, profit=%f WHERE id=%d;" \
              % (bamount, cost, samount, income, income-cost, idno)
        sql += "INSERT INTO trade (code, bprice, bamount, cost, bdate, sprice, samount, income, sdate, position) VALUES (%s, %.2f, %f, %.2f, '%s', %.2f, %f, %.2f, '%s', %f);"\
            % (code, bprice, balance['bamount'], balance['cost'], bdate, sprice, balance['samount'], balance['income'], sdate, balance['bamount']-balance['samount'])
        self.ps.execute(sql)
        
        
    
    def deletebyid(self, idno=''):
        sql = "DELETE FROM trade WHERE id=%s;" % idno
        self.ps.execute(sql)
    
    def deletebycode(self, code='600300'):
        sql = "DELETE FROM trade WHERE code='%s';" % code
        self.ps.execute(sql)
    
    
    def hold(self):
        sql = "SELECT COUNT(id), code, SUM(cost)/(SUM(bamount)+0.00001), SUM(bamount), SUM(cost), MAX(bdate), SUM(income)/(SUM(samount)+0.00001), SUM(samount), SUM(income), MAX(sdate), SUM(position), SUM(profit) FROM trade GROUP BY code ORDER BY MAX(bdate) DESC, MAX(sdate) DESC LIMIT 10;"
        res = self.ps.fetchall(sql)
        self._print(res)
    
    def display_set_code(self, ps=['code', '600300']):
        fs = self._analyse(ps)
        xg = XuanGu([self.code])
        xg.show_info()
        if fs['code'] != '':
            print "already set curent code is %s." % self.code
        

    def display(self, ps=['display', '600300', '5']):
        fs = self._analyse(ps)
        code = self.code
        limit = '5' if len(fs['other'])==0 else fs['other'][0]
        sql = "SELECT id, code, bprice, bamount, cost, bdate, sprice, samount, income, sdate, position, profit FROM trade WHERE code='%s' ORDER BY id DESC LIMIT %s;" % (code, limit)
        res = self.ps.fetchall(sql)
        self._print(res)
    
    def _print(self, rs=[]):
        n = len(rs)
        if n<1 : return
        print(' NO   id   code   bprice  bamount     cost       bdate     sprice  samount    income    sdate    position   profit')
        for i in range(n):
            r = rs[n-i-1]
            print('%3d %4d %7s %7.2f %7d %11.2f %11s %7.2f %7d %11.2f %11s %7d %9.2f'\
               % (i+1, r[0], r[1], r[2], r[3], r[4], r[5].strftime("%Y-%m-%d"), r[6], r[7], r[8], r[9].strftime("%Y-%m-%d"), r[10], r[11]))
            if (i+1)%5 == 0: print('')
        if (i+1)%5 > 0: print('')



#################################################################################################

def menu():
    print '''
 Exaple:
    buy(b)  code amount price [date]    #Example:  buy 600300 10000 6.66 [2015-12-30, default now]
    sale(s) code amount price [date]    #Example: sale 600300 10000 6.88 [2015-12-30, default now]
    hold(h)                             #Example: hold
    combine(cc) id1 id2 [...]           #Example: combine 25 26 [...]
    combinebycode(cbc) code [num]       #Example: combinebycode 600300 [default 2]
    display(d) code  [num]              #Example: diplay 600300 [default 5]
    deletebyid(dbi) id                  #Example: deletebyid 6
    deletebycode(dbc) code              #Example: deletebycode 600300
    code(c) [code]                      #Example: code [600300]                 display or set current code
    split id                            #Example: split 6
'''


def main():
    trade = Trade()
    while True:
        inp  = raw_input('[trade] >>> ').lower()
        if inp == '': continue
        inps = inp.split()
        i = inps[0]
        if   i in ['exit', 'e']:                break
        elif i in ['menu', 'm']:                menu()
        elif i in ['buy', 'b']:                 trade.buy(inps)
        elif i in ['sale', 's']:                trade.sale(inps)
        elif i in ['hold', 'h']:                trade.hold()
        elif i in ['combine', 'cc']:            trade.combine(inps)
        elif i in ['combinebycode', 'cbc']:     trade.combinebycode(inps)
        elif i in ['split']:                    trade.split(inps[1])
        elif i in ['display', 'd']:             trade.display(inps)
        elif i in ['deletebyid', 'dbi']:        trade.deletebyid(inps[1])
        elif i in ['deletebycode', 'dbc']:      trade.deletebycode(inps[1])
        elif i in ['code', 'c']:                trade.display_set_code(inps)
        else: print('your input content is wrong, please input again!')
    
    


if __name__ == '__main__':
    main()



