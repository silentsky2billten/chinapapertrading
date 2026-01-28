from snow.SnowTrader import     SnowTrader
from eastmoney.EastMoneyTrader import EastMoneyTrader
from strategy.strategy_top_low_n import strategy_top_low_n
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = webdriver.Chrome( options=chrome_options)

stock_trader = EastMoneyTrader(driver,group='组合一',min_amount =100,commission_fee=0.0004,transaction_fee=0.0004)
stock_strategy = strategy_top_low_n(
    trader=stock_trader,
    data_dir=r'E:\data\trade_stock_small_market',
    topOrlow='top',
    n=15,
    hold_check_pluscount=15,
    factor_col='factor',
    symbol_col='symbol',
    symbol_type='XXXXXX.MM',
    strategy='small'
    )
stock_strategy.trade()
zz1000_trader = EastMoneyTrader(driver,group='组合二',min_amount =100,commission_fee=0.0004,transaction_fee=0.0004)
zz1000_strategy = strategy_top_low_n(
    trader=zz1000_trader,
    data_dir=r'E:\data\trade_zz1000',
    topOrlow='top',
    n=15,
    hold_check_pluscount=15,
    factor_col='factor',
    symbol_col='symbol',
    symbol_type='XXXXXX.MM',
    strategy='zz1000'
    )
zz1000_strategy.trade()

driver.quit()
