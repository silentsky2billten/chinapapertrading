import os
import pandas as pd
import uuid 
import time
class Result:
    def __init__(self,code,msg,obj=None):
        self.code = code
        self.msg = msg
        self.obj = obj
    def __str__(self):
        return 'code:'+str(self.code)+' msg:'+self.msg
def get_last_file(dir):
    file_names = os.listdir(dir)
    sorted_file_names = sorted(file_names)
    if len(sorted_file_names) < 1:
        return None
    else:
        return os.path.join(dir,sorted_file_names[-1]) 
class strategy_top_low_n:
    def __init__(self,trader = None,data_dir ='E:\\data\\trader_tmp\\',topOrlow='top',n=15,hold_check_pluscount=5,factor_col='factor',symbol_col='symbol',symbol_type='XXXXXX',symbol_type_platform='XXXXXX',strategy='small'):
        self.dir = data_dir
        self.trader = trader
        self.topOrlow = topOrlow
        self.n = n
        self.data = None
        self.hold_check_data = None
        self.strategy = strategy
        self.factor_col = factor_col
        self.symbol_col = symbol_col
        self.symbol_type = symbol_type
        self.symbol_type_platform = symbol_type_platform
        self.hold_check_pluscount = hold_check_pluscount
        self.set_trade_data()
    def buy_per_cash(self):
        asset = self.trader.get_assets()
        cash = asset['cash']
        total_asset = asset['total_asset']
        per = total_asset / self.n
        buycash = min(cash, per)
        return buycash
        
    def set_trade_data(self):
        csv_file = get_last_file(self.dir)
        if csv_file is None:
            self.data = pd.DataFrame()
            self.hold_check_data = pd.DataFrame()
            return
        data = pd.read_csv(csv_file, dtype={self.symbol_col: str}, parse_dates=['date'])
        self.data = data.copy()
        self.data = self.data[self.data[self.factor_col] > 0]
        self.data = self.data.sort_values(by=self.factor_col, ascending=False if self.topOrlow == 'top' else True)
        self.hold_check_data = self.data.head(self.n + self.hold_check_pluscount)
        if self.symbol_type == 'XXXXXX':
            pass
        elif self.symbol_type[:3] == 'MM.':
            self.hold_check_data[self.symbol_col] = self.hold_check_data[self.symbol_col].str[3:]
        elif self.symbol_type[-3:] == '.MM':
            self.hold_check_data[self.symbol_col] = self.hold_check_data[self.symbol_col].str[:-3]
        elif self.symbol_type[:2] == 'MM':
            self.hold_check_data[self.symbol_col] = self.hold_check_data[self.symbol_col].str[2:]
        elif self.symbol_type[-2:] == 'MM':
            self.hold_check_data[self.symbol_col] = self.hold_check_data[self.symbol_col].str[:-2]
        else:
            pass
        self.data = self.hold_check_data.head(self.n)
    def sell(self):
        ps =  self.trader.get_positions()
        orderid=''
        print("ps",len(ps))
        for p in ps:
            #print(p['symbol'][2:],self.hold_check_data[self.symbol_col].values[0])
            p_symbol = p['symbol'] if self.symbol_type_platform == 'XXXXXX' else p['symbol'][2:]
            if p_symbol not in self.hold_check_data[self.symbol_col].values:
                count = p['amount']
                if count > 0:
                    orderid = self.strategy + '_s_' + str(uuid.uuid1())
                    self.trader.sell(p['symbol'],count)
                    print(Result(0,msg=f"sell success.{orderid} {p['symbol']},{count}" ))
        return orderid
    def buy(self,symbol,cash):
        ps =  self.trader.get_positions()
        holded = 0
        for p in ps:
            p_symbol = p['symbol'] if self.symbol_type_platform == 'XXXXXX' else p['symbol'][2:]
            if p_symbol == symbol:
                holded = p['market_value']
                break
        cash = cash - holded
        orderid = self.strategy + '_b_' + str(uuid.uuid1())
        r = self.trader.buy(symbol,cash)
        if r>0:
            print(Result(orderid,msg=f"buy success. {symbol},{cash}" ))
    def trade(self):
        self.sell()
        time.sleep(1)
        for symbol in self.data[self.symbol_col].values:
            self.buy(symbol,self.buy_per_cash())
