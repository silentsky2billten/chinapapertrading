from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
import time
class SnowTrader:
    def __init__(self, driver,group='small',min_amount = 100,commission_fee = 0.0001,transaction_fee = 0.0001):
        self.driver = driver
        self.min_amount = min_amount
        self.commission_fee = commission_fee
        self.transaction_fee = transaction_fee
        self.group = group
        self.set_group()
    def set_group(self):
        driver = self.driver
        all_windows = driver.window_handles
        for window in all_windows:
            driver.switch_to.window(window)
            if "雪球" in driver.title:
                break
        group_element = driver.find_elements(By.CLASS_NAME, "moni__tabs__controls")
        for g in group_element:
            print(g.text,self.group)
            a = g.find_element(By.TAG_NAME, "a")
            if a.text == self.group:
                if a.get_attribute("class") == "active":
                    pass
                else:
                    a.click()
                    time.sleep(2)
                moni__position__list__tabs = driver.find_element(By.CLASS_NAME, "moni__position__list__tabs")
                tabs = moni__position__list__tabs.find_elements(By.TAG_NAME, "a")
                for tab in tabs:
                    if tab.text == "持仓":
                        if tab.get_attribute("class") == "active":
                            break
                        else:
                            tab.click()
                            time.sleep(2)
                break
    def get_assets(self):
        driver = self.driver
        asssets={}
        total_assets_element = driver.find_element("xpath", "//span[text()='总资产']")
        next_sibling = total_assets_element.find_element("xpath", "following-sibling::*[1]")
        total_assets = next_sibling.text
        asssets['total_asset']=float(total_assets.replace(',',''))
        cash = driver.find_element("xpath", "//span[text()='现金']")
        next_sibling = cash.find_element("xpath", "following-sibling::*[1]")
        cash = next_sibling.text
        asssets['cash']=float(cash.replace(',',''))      
        return asssets
    def get_positions(self):
        positions=[]
        driver = self.driver
        position_div = driver.find_element(By.CLASS_NAME, "moni__position__list_position")
        trs = position_div.find_elements(By.TAG_NAME, "tr")
        for i,tr in enumerate(trs):
            position={}
            if i == 0:
                continue
            tds = tr.find_elements(By.TAG_NAME, "td")
            symbol_info = tds[0].find_elements(By.TAG_NAME, "div")
            symbol = symbol_info[1].text
            if len(symbol)==0:
                continue
            symbol_name = symbol_info[0].text
            # amount = tds[2].text
            position['symbol']=symbol
            position['symbol_name']=symbol_name
            position['market_value']=float(tds[3].text.replace(',',''))
            position['amount']=float(tds[4].text.replace(',',''))
            positions.append(position)
        return positions
    def buy(self, symbol, cash):
        if cash<1000:
            print(f"buy {symbol} failed. cash is {cash}")
            return -1
        asset = self.get_assets()
        if asset['cash']<cash:
            print(f"buy {symbol} failed. cash is {cash}")
            return -2
        driver = self.driver
        buy_button = driver.find_element("xpath", "//span[text()='买入']")
        buy_button.click()
        time.sleep(1)
        
        symbol_input = driver.find_element("xpath", "//input[@placeholder='搜索股票名称/代码/拼音']")
        symbol_input.send_keys(symbol)
        time.sleep(3)
        symbol_input.send_keys(Keys.ENTER)
        time.sleep(1)
        # 输入价格
        price_input = driver.find_elements("xpath", "//input[@placeholder='输入价格']")
        if not price_input:
            print(f"buy {symbol} failed. price_input is empty")
            return -3
        price = float(price_input[-1].get_attribute("value"))
        #price = float(price_input[-1].text)
        amount = int(cash/price/self.min_amount)*self.min_amount
        if amount<10:
            order = driver.find_elements(By.CLASS_NAME, "modal__order__performance")[-1] 
            cancle_button = order.find_elements(By.CLASS_NAME, "modal__confirm__cancle")[-1]
            cancle_button.click()
            time.sleep(1)
            print(f"buy {symbol} failed. amount is {amount}")
            return -4
        amount_input = driver.find_element("xpath", "//input[@placeholder='输入数量']")
        amount_input.send_keys(str(amount))
        commission_fee_input = driver.find_element("xpath", "//input[@placeholder='输入佣金率']")
        commission_fee_input.send_keys(Keys.CONTROL + "a")
        commission_fee_input.send_keys(str(self.commission_fee*1000))
        transaction_fee_input = driver.find_element("xpath", "//input[@placeholder='输入税率']")
        transaction_fee_input.send_keys(Keys.CONTROL + "a")
        transaction_fee_input.send_keys(str(self.transaction_fee*1000))
        # 查找并点击确认买入按钮（class为modal__confirm__submit）
        time.sleep(1)
        order = driver.find_elements(By.CLASS_NAME, "modal__order__performance")[-1] 
        confirm_button = order.find_elements(By.CLASS_NAME, "modal__confirm__submit")[-1]
        confirm_button.click()
        time.sleep(1)
        return 1
    def sell(self, symbol, amount):
        driver = self.driver
        sell_button = driver.find_element("xpath", "//span[text()='卖出']")
        sell_button.click()
        time.sleep(1)
        symbol_input = driver.find_element("xpath", "//input[@placeholder='搜索股票名称/代码/拼音']")
        symbol_input.send_keys(symbol)
        time.sleep(3)
        symbol_input.send_keys(Keys.ENTER)
        time.sleep(1)
        amount_input = driver.find_element("xpath", "//input[@placeholder='输入数量']")
        amount_input.send_keys(str(amount))
        commission_fee_input = driver.find_element("xpath", "//input[@placeholder='输入佣金率']")
        commission_fee_input.send_keys(Keys.CONTROL + "a")
        commission_fee_input.send_keys(str(self.commission_fee*1000))
        transaction_fee_input = driver.find_element("xpath", "//input[@placeholder='输入税率']")
        transaction_fee_input.send_keys(Keys.CONTROL + "a")
        transaction_fee_input.send_keys(str(self.transaction_fee*1000))
        time.sleep(1)
        order = driver.find_elements(By.CLASS_NAME, "modal__order__performance")[-1] 
        confirm_button = order.find_elements(By.CLASS_NAME, "modal__confirm__submit")[-1]
        confirm_button.click()
        time.sleep(1)
    def cancel_pending_orders(self):
        return
