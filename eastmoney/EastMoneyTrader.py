from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time,os
from selenium.webdriver.common.keys import Keys  
class EastMoneyTrader:
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
            if "东方财富" in driver.title:
                break
        
        zuhe = driver.find_element(By.ID, "ulzhlist")
        group_element = zuhe.find_elements(By.TAG_NAME, "li")
        for g in group_element:
            print(g.text,self.group)
            if g.text == self.group:
                if g.get_attribute("class") == "current":
                    pass
                else:
                    g.click()
                    time.sleep(2)
    def get_assets(self):
        asssets={}
        driver = self.driver
        zzc = driver.find_elements(By.CLASS_NAME, "bottom_name")
        for z in zzc:
            if z.text == "总资产":
                next_sibling = z.find_element("xpath", "following-sibling::*[1]")
                text = next_sibling.text
                asssets['total_asset']=float(text)
            if z.text == "可用余额":
                next_sibling = z.find_element("xpath", "following-sibling::*[1]")
                text = next_sibling.text
                asssets['cash']=float(text)  
        return asssets
    def get_positions(self):
        positions=[]
        driver = self.driver
        tab = driver.find_element(By.CSS_SELECTOR, '[data-type="ccxx"]')
        if tab.get_attribute("class") == "active":
            pass
        else:
            tab.click()
            time.sleep(2)
        info_list = driver.find_elements(By.CLASS_NAME, "info_list")[1]
        listpos = info_list.find_elements(By.CLASS_NAME, "content_ul")
        for i,ul in enumerate(listpos):
            position={}
            tds = ul.find_elements(By.TAG_NAME, "li")
            # <ul class="info_title">
            #                                     <li class="wd80">证券代码</li>0
            #                                     <li class="wd100">证券名称</li>1
            #                                     <li class="wd80">持仓数量</li>2
            #                                     <li class="wd80">可用数量</li>3
            #                                     <li class="wd80">摊薄成本价</li>4
            #                                     <li class="wd80">浮动盈亏</li>5
            #                                     <li class="wd100">浮动盈亏比</li>6
            #                                     <li class="wd100">市价</li>7
            #                                     <li class="wd100">市值</li>8
            #                                 </ul>
            position['symbol']=ul[0].text
            position['symbol_name']=ul[1].text
            position['market_value']=float(ul[8].text)
            position['amount']=float(ul[2].text)
            position['canuse_amount']=float(ul[3].text)
            positions.append(position)
        return positions
    def buy(self, symbol, cash):
        driver = self.driver
        if cash<1000:
            print(f"buy {symbol} failed. cash is {cash}")
            return -1
        asset = self.get_assets()
        if asset['cash']<cash:
            print(f"buy {symbol} failed. cash is {cash}")
            return -2
        tab_buy =driver.find_element(By.CLASS_NAME, 'tab_buy')
        if tab_buy.get_attribute("class") == "active":
            pass
        else:
            tab_buy.click()
            time.sleep(2)
        # 输入代码
        symbol_input = driver.find_element(By.ID, "futcode")
        symbol_input.send_keys(Keys.CONTROL + "a")
        symbol_input.send_keys(Keys.BACK_SPACE)
        time.sleep(0.1)
        symbol_input.send_keys(symbol)
        time.sleep(1)
        select_element = symbol_input.find_element(By.XPATH, 'following-sibling::*[1]')
        table =select_element.find_element(By.CLASS_NAME, "sg2017table")
        tr0 = table.find_element(By.TAG_NAME, "tr")
        tr0.click()
        time.sleep(2)
        price_element = driver.find_element(By.ID, "price")
        print(price_element.get_attribute("value"))
        price = float(price_element.get_attribute("value"))    
        amount = int(cash/price/self.min_amount)*self.min_amount
        if amount<self.min_amount:
            print(f"buy {symbol} failed. amount is {amount}")
            return -4
        # 输入数量
        amount_element = driver.find_element(By.ID, "codenumber")
        amount_element.send_keys(Keys.CONTROL + "a")
        amount_element.send_keys(str(amount))
        time.sleep(0.5)
        buy_button = driver.find_element(By.ID, 'btnOrder')
        buy_button.click()
        time.sleep(5)
        return 1
    def sell(self, symbol, amount):
        driver = self.driver
        tab_sell =driver.find_element(By.CLASS_NAME, 'tab_sell')
        if tab_sell.get_attribute("class") == "active":
            pass
        else:
            tab_sell.click()
            time.sleep(2)
        # 输入代码
        symbol_input = driver.find_element(By.ID, "futcode")
        symbol_input.send_keys(Keys.CONTROL + "a")
        symbol_input.send_keys(Keys.BACK_SPACE)
        time.sleep(0.1)
        symbol_input.send_keys(symbol)
        time.sleep(1)
        select_element = symbol_input.find_element(By.XPATH, 'following-sibling::*[1]')
        table =select_element.find_element(By.CLASS_NAME, "sg2017table")
        tr0 = table.find_element(By.TAG_NAME, "tr")
        tr0.click()
        time.sleep(0.5)
        # 输入数量
        amount_element = driver.find_element(By.ID, "codenumber")
        amount_element.send_keys(Keys.CONTROL + "a")
        amount_element.send_keys(Keys.BACK_SPACE)
        time.sleep(0.1)
        amount_element.send_keys(str(amount))
        time.sleep(0.5)
        buy_button = driver.find_element(By.ID, 'btnOrder')
        buy_button.click()
        time.sleep(5)
        return 1
